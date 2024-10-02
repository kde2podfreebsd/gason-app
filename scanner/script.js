const video = document.getElementById('video');
const canvasElement = document.getElementById('canvas');
const canvas = canvasElement.getContext('2d');
const modal = document.getElementById('modal');
const overlay = document.getElementById('overlay');
const modalMessage = document.getElementById('modal-message');
const closeModalButton = document.getElementById('close-modal');

const validUsers = [{username: 'value', chat_id: 'value'}];

const botToken = '<tg-bot-token>';
const channelId = '@nagasone';

async function checkTelegramSubscription(chatId) {
    const response = await fetch(`https://api.telegram.org/bot${botToken}/getChatMember?chat_id=${channelId}&user_id=${chatId}`);
    const data = await response.json();
    return data.result && (data.result.status === 'member' || data.result.status === 'administrator' || data.result.status === 'creator');
}

navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function(stream) {
    video.srcObject = stream;
    video.setAttribute("playsinline", true);
    video.play();
    requestAnimationFrame(tick);
});

async function tick() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

        const imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        const qrCode = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert",
        });

        if (qrCode) {
            const qrData = qrCode.data;
            if (/^https:\/\/t\.me\/\w+$/.test(qrData)) {
                const username = qrData.split('/').pop().toLowerCase();
                const user = validUsers.find(user => user.username.toLowerCase() === username);

                if (user) {
                    const isSubscribed = await checkTelegramSubscription(user.chat_id);

                    let message = `1) Юзер ${user ? 'успел' : 'не успел'} в списки.\n`;
                    message += `2) Юзер ${isSubscribed ? 'подписан' : 'не подписан'} на канал.`;

                    showModal(message, isSubscribed);
                } else {
                    showModal('Юзер не найден в списках.', false);
                }
            } else {
                showModal('QR code does not match the expected pattern.', false);
            }
        }
    }
    requestAnimationFrame(tick);
}

function showModal(message, isSuccess) {
    modalMessage.textContent = message;
    if (isSuccess) {
        modal.classList.add('modal-success');
        modal.classList.remove('modal-error');
    } else {
        modal.classList.add('modal-error');
        modal.classList.remove('modal-success');
    }
    overlay.style.display = 'block';
    modal.style.display = 'block';
}

closeModalButton.addEventListener('click', () => {
    modal.style.display = 'none';
    overlay.style.display = 'none';
});

modal.style.display = 'none';
overlay.style.display = 'none';