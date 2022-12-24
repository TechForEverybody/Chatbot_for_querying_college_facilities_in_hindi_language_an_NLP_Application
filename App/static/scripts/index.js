function renderChatsonScreen(direction, message,time) {
	let rendering_content = `
    <div class="chat ${direction}">
    ${message}
	<div class="time">${time.substring(0,5)}</div>
    </div>
    `;
	let chatContent = document.getElementById("chatContent");
	let isscrolltime =chatContent.scrollHeight -chatContent.scrollTop -chatContent.clientHeight ==0 ||chatContent.scrollHeight - chatContent.scrollTop -chatContent.clientHeight <150;


	chatContent.innerHTML = chatContent.innerHTML +rendering_content;
	if (isscrolltime) {
		chatContent.scrollTop = chatContent.scrollHeight;
		console.log("scrolled");
	}
}
let notifier_music = new Audio("../../static/music/notification_sound.mp3");

async function getResponse(event) {
	event.preventDefault();
	question = document.getElementById("question");
	console.log(question.value);
	if (question.value == "") {
		window.alert("Please Enter any query first");
	} else {
		renderChatsonScreen("right", question.value,new Date().toTimeString());
		try {
			let response = await fetch("/getresponse", {
				method: "POST",
				headers: {
					"Content-Type": "Application/json",
				},
				body: JSON.stringify({
					question: question.value,
				}),
			});
			let result = await response.json();
			console.log(result);
			outputsData=JSON.parse(result.output)
			console.log(outputsData);
			if (!!outputsData) {
				document.getElementById('container').innerHTML=`
				<div class="nlptask validation">
				<h3>script validation</h3>
				<div class="output">

				${outputsData.validation?`
				<img
					src="https://png.pngtree.com/png-vector/20190115/ourlarge/pngtree-vector-valid-stamp-icon-png-image_319812.jpg"
					alt=""
				/>
				`:`
				<img
				src="https://thumbs.dreamstime.com/b/invalid-seal-print-corroded-texture-red-vector-rubber-label-dust-text-tag-placed-double-parallel-lines-131842910.jpg"
				alt=""
				/>
				`}
				</div>
			</div>

			<div class="nlptask filtration">
				<h3>filtration</h3>
				<div class="output"> ${outputsData.filtration} </div>
			</div>
			<div class="nlptask tokenization">
				<h3>tokenization</h3>
				<div class="output">[ ${outputsData.tokenization} ]</div>
			</div>
			<div class="nlptask vecotorization">
				<h3>vecotorization</h3>
				<div class="output">[${outputsData.vectorization}]</div>
			</div>
				`
			} else {
				
			}
			notifier_music.play();
			renderChatsonScreen("left", result.response,new Date().toTimeString());
			// window.alert("result is fetched and shown below");
			// window.alert(result.response);
			question.value = "";
			document.getElementById('suggested').innerHTML=``
			setTimeout(() => {
				notifier_music.pause();
			}, 1000);
		} catch (error) {
			console.log(error);
		}
	}
}
async function getQuestionSuggestion() {
	question = document.getElementById("question");
	console.log(question.value);
	if (question.value.length<5) {
		document.getElementById('suggested').innerHTML=``
	} else {
		try {
			let response = await fetch("/getsuggestion", {
				method: "POST",
				headers: {
					"Content-Type": "Application/json",
				},
				body: JSON.stringify({
					question: question.value,
				}),
			});
			let result = await response.json();
			console.log(result);
			let rendering_content=``
			if (result.response.length>0) {
				rendering_content=`					<p>suggestion:</p>
				`
				result.response.forEach(element => {
					rendering_content=rendering_content+`
					<button onclick="updateQuestion('${element}')">${element}</button>
					`
				});
			}
			document.getElementById('suggested').innerHTML=rendering_content
		} catch (error) {
			console.log(error);
		}
	}
}

setInterval(() => {
	getQuestionSuggestion();
}, 3000);


function updateQuestion(value) {
	console.log(value);
	document.getElementById("question").value=value;
	document.getElementById('submitbutton').click();
}