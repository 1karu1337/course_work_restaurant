let cart = [];
let userRole = null;

// --- 1. Навигация ---
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId + '-page').classList.add('active');
    
    if(pageId === 'menu') loadMenu();
    if(pageId === 'orders') loadOrders();
}

// --- 2. Авторизация ---
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    const response = await fetch('/auth/login', { method: 'POST', body: formData });
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        await checkUser();
        showPage('menu');
    } else {
        alert('Неверный логин или пароль');
    }
});

async function checkUser() {
    const token = localStorage.getItem('token');
    if (!token) {
        renderAuthUI(false);
        return;
    }
    const response = await fetch('/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) {
        const user = await response.json();
        userRole = user.role_id; // 4 - админ, 1 - клиент
        renderAuthUI(true, user.username);
    } else {
        logout();
    }
}

function renderAuthUI(isAuth, username = '') {
    const area = document.getElementById('auth-area');
    const adminLink = document.getElementById('admin-link');
    
    if (isAuth) {
        area.innerHTML = `<span>👤 ${username}</span> <button onclick="logout()">Выйти</button>`;
        if (userRole >= 3) { // Менеджер или Админ
            adminLink.innerHTML = `<button onclick="showPage('admin')" style="background: #57606f">Админка</button>`;
        }
    } else {
        area.innerHTML = `<button onclick="showPage('login')">Войти</button>`;
        adminLink.innerHTML = '';
    }
}

function logout() {
    localStorage.removeItem('token');
    userRole = null;
    renderAuthUI(false);
    showPage('menu');
}

// --- 3. Работа с Меню и Корзиной ---
async function loadMenu() {
    const grid = document.getElementById('menu-grid');
    const response = await fetch('/menu/items');
    const items = await response.json();

    grid.innerHTML = items.map(item => `
        <div class="card">
            <h3>${item.name}</h3>
            <p>${item.description || ''}</p>
            <div style="display:flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.2rem; font-weight: bold;">${item.price} ₽</span>
                <button class="btn-main" style="width:auto;" onclick="addToCart(${item.id}, '${item.name}')" ${!item.is_available ? 'disabled' : ''}>
                    ${item.is_available ? 'Добавить' : 'Нет в наличии'}
                </button>
            </div>
        </div>
    `).join('');
}

function addToCart(id, name) {
    cart.push({ id, name });
    document.getElementById('cart-info').innerText = `Корзина: ${cart.length} блюд`;
    document.getElementById('order-confirm-bar').style.display = 'block';
}

async function placeOrder() {
    const token = localStorage.getItem('token');
    if (!token) { alert('Войдите, чтобы сделать заказ'); showPage('login'); return; }

    const orderData = {
        table_id: null,
        items: cart.map(item => ({ menu_item_id: item.id, quantity: 1 }))
    };

    const response = await fetch('/orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(orderData)
    });

    if (response.ok) {
        alert('Заказ принят! Приятного аппетита.');
        cart = [];
        document.getElementById('cart-info').innerText = `Корзина: 0 блюд`;
        document.getElementById('order-confirm-bar').style.display = 'none';
        showPage('orders');
    }
}

// --- 4. История заказов ---
async function loadOrders() {
    const token = localStorage.getItem('token');
    if (!token) { document.getElementById('orders-list').innerHTML = '<p>Войдите, чтобы увидеть историю</p>'; return; }

    const response = await fetch('/orders/my', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const orders = await response.json();
    const list = document.getElementById('orders-list');

    list.innerHTML = orders.map(o => `
        <div class="card" style="margin-bottom: 15px;">
            <div style="display:flex; justify-content: space-between;">
                <strong>Заказ №${o.id}</strong>
                <span class="badge status-${o.status}">${o.status}</span>
            </div>
            <div style="margin-top: 10px; font-size: 0.9rem;">
                ${o.items.map(i => `• Блюдо ID ${i.menu_item_id} (цена: ${i.price_at_order} ₽)`).join('<br>')}
            </div>
            <div style="margin-top: 10px; text-align: right; color: #666;">
                ${new Date(o.created_at).toLocaleString()}
            </div>
        </div>
    `).join('');
}

// --- 5. Админка: Экспорт и Бэкап (Требования №2, №3) ---
async function exportData(format) {
    const token = localStorage.getItem('token');
    // Просто переходим по ссылке, браузер сам скачает файл
    window.location.href = `/export/menu?format=${format}&token=${token}`; 
    // Примечание: для скачивания файлов через API с JWT обычно токен передают в Query, 
    // если не хотят заморачиваться с Blob в JS.
}

async function createBackup() {
    const token = localStorage.getItem('token');
    const status = document.getElementById('backup-status');
    status.innerText = 'Выполняется создание резервной копии...';

    const response = await fetch('/admin/backup', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const data = await response.json();
    if (response.ok) {
        status.innerHTML = `<span style="color: green;">✅ Бэкап создан: ${data.filename} (${data.size_kb} KB)</span>`;
    } else {
        status.innerHTML = `<span style="color: red;">❌ Ошибка: ${data.detail}</span>`;
    }
}

// Инициализация
checkUser();
loadMenu();