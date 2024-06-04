let inputRequest = $('#chat_input');
let submitButton = $('#send_button');
let voice_input = $('#voice_input');
let fileInput = $('#fileInput');
let counseling = $('#counseling');
let requestCount = 0;
let is_upgraded = false;
let imageUrl = null;

let response_List = [];
let actual_ans = [];
let predTwo=false;
let diseaseList=[0,1,2];
let finalDisease="";
const questions_list = [
    "Hello! I'm a disease diagnosis chatbot. To begin, I'll ask you a series of questions about your symptoms and health profile. Please answer them accurately.",
    "Can you identify the symptoms you are experiencing?"
];


$(document).ready(function () {

        ask_questions(requestCount);
        requestCount++;

        setTimeout(() => {
            ask_questions(requestCount);
            requestCount++;
        }, 400);

        imageUrl = $('#profile').val();
        if (inputRequest.val().length == 0) {
            submitButton.prop("disabled", true);
        }

        inputRequest.on("input", function () {
            $.trim($(this).val()) != "" ? submitButton.prop("disabled", false) : submitButton.prop("disabled", true);
        });

        $('#chatForm').submit(function (event) {
            event.preventDefault();
            var chatData = new FormData(this);
            chatbot(chatData, requestCount);
            requestCount++;
        });

        inputRequest.on("keypress", function (event) {
            // Check if the pressed key is Enter (key code 13)
            if (event.which === 13) {
                if (inputRequest.val().length > 0) {
                    $("#chatForm").submit();
                    event.preventDefault();
                }
            }
        });


        $("#voice_input").on("click", function () {
            inputRequest.val(null);
            submitButton.prop("disabled", true)
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function (stream) {
                    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

                    recognition.lang = 'en-US';
                    recognition.start();
                    inputRequest.attr('placeholder', 'Recognizing ...');

                    recognition.onresult = function (event) {
                        inputRequest.attr('placeholder', 'Message ...');
                        const transcript = event.results[0][0].transcript;
                        inputRequest.val(transcript);
                        $.trim(transcript) != "" ? submitButton.prop("disabled", false) : submitButton.prop("disabled", true);

                    };

                    recognition.onend = function () {
                        inputRequest.attr('placeholder', 'Message ...');
                        stream.getTracks().forEach(track => track.stop()); // Stop the microphone stream
                    };
                })
                .catch(function (error) {
                    console.error('Error accessing microphone:', error);
                    alert('Please grant microphone permissions to use this feature.');
                });
        });

        $('#new_chat').click(() => window.location.reload());

        $("#file_button").click(function () {
            $("#fileInput").click();
        });

        $("#fileInput").change(function (event) {
            $("#chatForm").submit();
            event.preventDefault();
        });
});




const chatbot =async (chatData, index) => {
    let chat = Object.fromEntries(chatData);
    var request = requestDiv(chat);
    var inputValue = $.trim(chat.chat_input);
    console.log("Index:",index)
    if(inputValue!="no")
    {
        if(inputValue==="yes")
        {
            finalDisease=appendWithComma(finalDisease,diseaseList[index])
        }
        else{
         finalDisease=appendWithComma(finalDisease,inputValue)
        }
        console.log(finalDisease)

    }
    var response = responseDiv(index);
    if (inputValue != "") {
        delete chat.fileInput;
    }
    if (inputValue != "" || chat.fileInput.size > 0) {
        $('.chat-block').append(request);
        $('#chat_input').val("");
        $('#send_button').prop("disabled", true);
//        const formatted_value = formatted_input(inputValue);
        response_List.push(inputValue);
        actual_ans.push(inputValue);
        const lastIndex = questions_list.length - 1;


        if(index===2)
        {
            const myListJson = JSON.stringify(response_List);
           await initialRequest({ 'response': myListJson },index)
        }
        else if (index > lastIndex) {
            $('.chat-block').append(response);
            const inputBlock = document.querySelector('.input-block');
            inputBlock.style.display = 'none';
            const myListJson = JSON.stringify(response_List);
            console.log(finalDisease)
            sendRequest({ 'response': finalDisease}, index, false)
        }
         else {
            ask_questions(index);
        }
        scrollToBottom();
    }


}

const initialRequest=async(formData,index)=>{
   await PostRequest(predictInitialDiseaseApi, formData,
            (response) => {
                console.log("responce:",response)
                for(var i=0;i<response.message.length;i++)
                {
                    questions_list.push(`Do you have ${response.message[i]} ?`)
                    diseaseList.push(response.message[i])
                }
                ask_questions(index)
            }

        );

}

const sendRequest = (formData, index, has_file) => {
    PostRequest(predictDiseaseApi, formData,
        (response) => {
            if (response.status) {

                const message = `Based on your responses, it seems like you may be experiencing symptoms of a ${response.message}.I strongly recommend consulting a doctor for a proper diagnosis and treatment plan.`;
                typeText(".response .response-text-" + index + "", message, 0, 20);
                $(`.response-text-${index} .spinner-grow`).remove();

                setTimeout(() => {
                    appendDoctor(response.data);
                }, 5000);
            } else {
                const message = `Based on your responses, it seems like you may be experiencing symptoms of a ${response.message}. However, I don't have a specialized doctor for ${response.message}, so I apologize for any inconvenience.`;
                typeText(".response .response-text-" + index + "", message, 0, 20);
                $(`.response-text-${index} .spinner-grow`).remove();
            }
            setTimeout(() => {
                let serializedList1 = encodeURIComponent(JSON.stringify(questions_list));
                let serializedList2 = encodeURIComponent(JSON.stringify(actual_ans));
                let prob=response.probability;
                let probabi = prob.toFixed(2);
                let url = `/generate_pdf_view/?questions=${serializedList1}&answers=${serializedList2}&disease=${response.message}&probability=${probabi}`;
                let div = `<div class ="ms-5">
                <a  href="${url}">Download Report</a>
                </div>`;
                $('.chat-block').append(div);
            }, 4000);

        }, has_file
    );
}

const requestDiv = (chatData, view_chat = false) => {

    var content; // Variable to store the content (image or text)

    if (view_chat) {
        content = chatData;
    } else {
        content = chatData.chat_input;
    }

    // Create the request HTML
    var request = `
        <div class="pe-2 ms-5 mb-4 d-flex justify-content-end align-items-start request">
            <div class="ms-5">
                <img src=/media/${imageUrl} alt="User Avatar" class="object-fit-fill rounded-circle border border-2 p-1 me-2" width="40" height="40">
            </div>
            <div class="card d-inline-block p-4 bg-light">
                ${content}
            </div>
        </div>
    `;

    return request;
}


const responseDiv = (index) => {
    var response = `
    <div class="pe-2 me-5 mb-4 d-flex justify-content-start align-items-start response">
    <div>
        <img src="/media/gpt_logo.png" alt="Chatbot Avatar"
            class="object-fit-fill rounded-circle  border border-1 me-2 " width="40" height="40">
    </div>
    <div class="card d-inline-block p-4 bg-transparent response-text-`+ index + `"> 
    <div class="spinner-grow spinner-grow-sm" role="status">
    </div>
    </div>
    </div>`;

    return response;
}


// Function to simulate typing effect
const typeText = (element, text, index, speed) => {
    if (index < text.length) {
        $(element).append(text[index]);
        index++;
        setTimeout(function () {
            typeText(element, text, index, speed);
        }, speed);
    }
    scrollToBottom();
}

const scrollToBottom = () => {
    var container = $(".scroll");
    container.scrollTop(container.prop("scrollHeight"));
}


function openFileInput() {
    document.getElementById('fileInput').click();
}

function handleFileSelect(input) {
    // Handle the selected file here
    // You can access the selected file using input.files[0]
    console.log("Selected file:", input.files[0].name);
}


const ask_questions = (index) => {
    var response = responseDiv(index);
    $('.chat-block').append(response);
    typeText(".response .response-text-" + index + "", questions_list[index], 0, 20);
    $(`.response-text-${index} .spinner-grow`).remove();
}

//const formatted_input = (input) => {
//    let val = 0;
//    const lowerCaseInput = input.toLowerCase();
//    if (lowerCaseInput === "yes") {
//        val = 1;
//    } else if (lowerCaseInput === "no") {
//        val = 0;
//    } else if (lowerCaseInput === "high") {
//        val = 3;
//    } else if (lowerCaseInput === "normal") {
//        val = 2;
//    } else if (lowerCaseInput === "low") {
//        val = 1;
//    }
//    return val;
//}

const appendDoctor = (data) => {
    let div = `<div class="row">`;

    data.forEach(element => {
        div += `
        <div class="col-12 col-md-6 col-lg-6 col-sm-12 my-1">
        <div class="card mt-3 rounded h-100 ">
            <div class="row g-0 d-flex align-items-center">
                <div class="col-md-4">
                    <img src="${element.image}" class="object-fit-cover m-2 rounded shadow-sm alt=" Crop Image"
                        height="160" width="160">
                </div>
                <div class="col-md-8 ">
                    <div class="card-body">

                        <h5 class="card-title">${element.name}</h5>

                        <p class="badge rounded-pill text-bg-dark p-2 px-3 mt-2">${element.gender}</p>
                        <p class="card-text">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-geo-alt" viewBox="0 0 16 16">
                                <path
                                    d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A32 32 0 0 1 8 14.58a32 32 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10" />
                                <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4m0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />
                            </svg>
                            <small class="text-body-secondary">${element.address}</small>
                        </p>
                    </div>
                </div>
                <div class="card-footer d-flex bg-transparent mt-1 d-flex justify-content-center">
                    <div class="me-2 border-end pe-5">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-telephone mx-2" viewBox="0 0 16 16">
                            <path
                                d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58zM1.884.511a1.745 1.745 0 0 1 2.612.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z" />
                        </svg>
                        ${element.contact}
                    </div>

                    <div class="me-2  pe-5">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-envelope-at mx-2" viewBox="0 0 16 16">
                            <path
                                d="M2 2a2 2 0 0 0-2 2v8.01A2 2 0 0 0 2 14h5.5a.5.5 0 0 0 0-1H2a1 1 0 0 1-.966-.741l5.64-3.471L8 9.583l7-4.2V8.5a.5.5 0 0 0 1 0V4a2 2 0 0 0-2-2zm3.708 6.208L1 11.105V5.383zM1 4.217V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v.217l-7 4.2z" />
                            <path
                                d="M14.247 14.269c1.01 0 1.587-.857 1.587-2.025v-.21C15.834 10.43 14.64 9 12.52 9h-.035C10.42 9 9 10.36 9 12.432v.214C9 14.82 10.438 16 12.358 16h.044c.594 0 1.018-.074 1.237-.175v-.73c-.245.11-.673.18-1.18.18h-.044c-1.334 0-2.571-.788-2.571-2.655v-.157c0-1.657 1.058-2.724 2.64-2.724h.04c1.535 0 2.484 1.05 2.484 2.326v.118c0 .975-.324 1.39-.639 1.39-.232 0-.41-.148-.41-.42v-2.19h-.906v.569h-.03c-.084-.298-.368-.63-.954-.63-.778 0-1.259.555-1.259 1.4v.528c0 .892.49 1.434 1.26 1.434.471 0 .896-.227 1.014-.643h.043c.118.42.617.648 1.12.648m-2.453-1.588v-.227c0-.546.227-.791.573-.791.297 0 .572.192.572.708v.367c0 .573-.253.744-.564.744-.354 0-.581-.215-.581-.8Z" />
                        </svg>
                        ${element.email}
                    </div>
                </div>
            </div>
        </div>
    </div>
        `;
    });

    div += `</div>`;
    $('.chat-block').append(div);

}

const download_report = () => {
    alert('Report')
    const data = { 'questions': questions_list, 'answers': actual_ans };
}
function appendWithComma(originalString, wordToAdd) {
    if (originalString === "") {
        return wordToAdd;
    } else {
        return originalString + ", " + wordToAdd;
    }
}