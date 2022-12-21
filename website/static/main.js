const emojiBtn = document.querySelector('#btn-emoji');
const picker = new EmojiButton();
const btnChat = document.querySelector('.btn-chat');
const popup = document.querySelector('.popup-chat');

const btnSend = document.querySelector('.btn-send');
const chatWindow = document.querySelector('.chat-window');
const txtInput = document.querySelector('#txtInput');

const form = document.querySelector('form');

const scrollv = document.getElementById('scrollv')

const  chatBotChat = async ( message )=>{
    url='/get'
    console.log(message)
    const res =await fetch(url,{
             method:"POST",
             mode:'no-cors',

             body  :message 
            })
const botMessage = await res.text()
    console.log(botMessage)
    return botMessage
}

const scrollSmoothlyToBottom = (id) => {
    const element = $('#chat-window');
    element.animate({
        scrollTop: element.prop("scrollHeight")
    }, 500);
}

// Emoji selection
window.addEventListener('DOMContentLoaded', () => {

    picker.on('emoji', emoji => {
        document.querySelector('input').value += emoji;
    });

    emojiBtn.addEventListener('click', () => {
        picker.togglePicker(emojiBtn);
    });
});

btnChat.addEventListener('click', ()=>{
    popup.classList.toggle('showWindow');
})

btnSend.addEventListener('click', async(event)=>{

    event.preventDefault()
    let userInput = txtInput.value;

let temp = `<div class="out-msg">
<span class="my-msg">${userInput}</span>
<img src="../static/images/me.jpeg" class="picture" />
</div>`;

chatWindow.insertAdjacentHTML("beforeend", temp);
txtInput.value = ''
    scrollSmoothlyToBottom()
    txtInput.value = '';

   const botResponse = await chatBotChat(userInput)

                    let tempBot = `<div class="out-msgbot">
                    <img src="../static/images/bot.jpeg" class="picture">
                    <span class="my-msg">${botResponse}</span>
                    </div>`;

                    chatWindow.insertAdjacentHTML("beforeend", tempBot);
                     scrollSmoothlyToBottom()
})