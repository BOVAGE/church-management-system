const playBtn = document.getElementById('play');
const content = document.querySelector('.content');

function text_to_speech(text, startOver=true){
    if (startOver) {
        speechSynthesis.cancel();
    }
    let utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = speechSynthesis.getVoices()[0];
    speechSynthesis.speak(utterance);
}

playBtn.addEventListener('click', text_to_speech.bind(null, content.textContent));

// stops the sound once on page reload
window.addEventListener('beforeunload',() => speechSynthesis.cancel(), false);


