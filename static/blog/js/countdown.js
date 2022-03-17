const DAYS = document.getElementById("days");
const HOURS = document.getElementById("hours");
const MINS = document.getElementById("mins");
const SECS = document.getElementById("secs");
const datedetail = document.getElementById("countdown-date");

// let date = "25 Dec 2021";
let date = datedetail.textContent;

function formatTime(time) {
	return time < 10? `0${time}`: time;
}

function countdown() {
	countdownDate = new Date(date);
	if (new Date() >= countdownDate)	{
        console.log('Countdown Completed')
		return ; 
	}
	let totalSeconds = (countdownDate - new Date()) / 1000;
	let days = Math.floor(totalSeconds / 3600 / 24);
	let hours = Math.floor(totalSeconds / 3600) % 24;
	let minutes = Math.floor(totalSeconds / 60) % 60;
	let seconds = Math.floor(totalSeconds) % 60;
	DAYS.innerHTML = days + ` <span class = "units">Days</span>`;
	HOURS.innerHTML = formatTime(hours) + ` <span class = "units">Hours</span>`;
	MINS.innerHTML = formatTime(minutes) + ` <span class = "units">Minutes</span>`;
	SECS.innerHTML = formatTime(seconds) + ` <span class = "units">Seconds</span>`;
	setTimeout(() => {
		countdown();
	}, 1000);
}

if (date != false) {
	countdown();
}