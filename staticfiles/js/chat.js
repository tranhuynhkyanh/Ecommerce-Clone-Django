const id = JSON.parse(document.getElementById('json-username').textContent)
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

const socket = new WebSocket("wss://"+ window.location.host+ "/chat/"+id+"/");

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    const date = Date.now()
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `  
        <li class="clearfix">
            <div class="message-data text-right">
                <span class="message-data-time">${date}</span>
                <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
            </div>
            <div class="message other-message float-right"> ${data.message} </div>
         </li>`
    }else{
        document.querySelector('#chat-body').innerHTML += `  
        <li class="clearfix">
            <div class="message-data">
                <span class="message-data-time">${date}</span>
            </div>
            <div class="message my-message">${data.message}</div>                                    
        </li>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;
    console.log(1)
    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver
    }));

    message_input.value = '';
}
