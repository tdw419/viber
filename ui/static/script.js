
const debateContainer = document.getElementById('debate-container');

const messages = [
    "Agent 1: Hello, everyone. I'd like to start by saying that AI is the future.",
    "Agent 2: I agree, but we need to be careful about the ethical implications.",
    "Agent 1: A valid point. However, the potential benefits outweigh the risks.",
];

let i = 0;
function addMessage() {
    if (i < messages.length) {
        const p = document.createElement('p');
        p.textContent = messages[i];
        debateContainer.appendChild(p);
        i++;
        setTimeout(addMessage, 2000);
    }
}

addMessage();
