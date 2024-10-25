let allowedUserIds = []; // Initialize an empty array

window.onload = function() {
    // Fetch allowed user IDs from the JSON file
    fetch('auth_users.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            allowedUserIds = data.allowedUserIds; // Assign the fetched user IDs

            const userData = Telegram.WebApp.initDataUnsafe?.user;

            if (window.innerWidth > 768) {
                document.body.innerHTML = "<div style='color: #fff; text-align: center; padding: 20px;'><h1>Melodamore is only available on mobile devices.</h1><p>Please open this app on a mobile phone or tablet.</p></div>";
                return;
            }

            if (userData && allowedUserIds.includes(userData.id)) {
                // Authorized user, show the main app content and tab bar
                document.querySelector('.tab-bar').style.display = 'flex';

                // Set home as the default active tab on first load
                switchTab('home');

                // Populate profile information
                document.getElementById('name').textContent = `${userData.first_name} ${userData.last_name || ""}`;
                document.getElementById('username').textContent = userData.username || "N/A";
                document.getElementById('user-id').textContent = userData.id;

                if (userData.photo_url) {
                    document.getElementById('profile-pic').src = userData.photo_url;
                }
            } else {
                // Unauthorized user, show access denied message only
                document.getElementById('access-denied').classList.add('active');
            }
        })
        .catch(error => {
            console.error('Error fetching allowed users:', error);
        });
};

function switchTab(tabId) {
    // Hide all containers
    document.querySelectorAll('.container').forEach(container => {
        container.classList.remove('active');
    });
    // Show the selected container
    document.getElementById(tabId).classList.add('active');

    // Update tab styles to indicate the active tab
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active-tab');
    });
    document.querySelector(`.tab[onclick="switchTab('${tabId}')"]`).classList.add('active-tab');
}

function messageSupport() {
    const userId = Telegram.WebApp.initDataUnsafe?.user?.id || "unknown";
    const message = `I want to access the app. My ID is ${userId}.`;
    const encodedMessage = encodeURIComponent(message);
    window.location.href = `https://t.me/melodamore?text=${encodedMessage}`;
}