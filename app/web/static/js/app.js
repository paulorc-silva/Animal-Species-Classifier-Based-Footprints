let image = document.getElementById('image');
let previewImg = document.getElementById('preview-img');
let preview = document.querySelector('.preview');
let closeBtn = document.querySelector('.close');
let uploadBtn = document.getElementById('upload-image');
let sendBtn = document.getElementById('send-image');

onload = function () {
    closeBtn.style.display = 'none';
};
onload();

function handleImageChange() {
    const file = image.files[0];

    if(file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            previewImg.setAttribute('src', e.target.result);
            preview.className = 'preview active';
            preview.classList.toggle('animate');
            closeBtn.style.display = 'block';
            uploadBtn.style.display = 'none';
            sendBtn.style.display = 'block';

            setTimeout(() => {
                if(preview.classList.contains('animate')) {
                    preview.classList.toggle('animate');
                }
            }, 3000);
        };

        reader.readAsDataURL(file);
    }
    else {
        previewImg.setAttribute('src', '');
        preview.className = 'preview';
    }
}

function closeIt() {
    previewImg.setAttribute('src', '');
    image.value = '';
    preview.className = 'preview';
    closeBtn.style.display = 'none';
    uploadBtn.style.display = 'block';
    sendBtn.style.display = 'none';
};

function showPage(page) { 
    var loadPage = document.getElementById('load-page');
    var uploadPage = document.getElementById('upload-page');
    var resultPage = document.getElementById('result-page');

    loadPage.style.bottom = '0';
    
    setTimeout(function() { 
        loadPage.style.bottom = '-100%';
        
        if (page == 'upload') {
            uploadPage.style.display = 'flex';
            resultPage.style.display = 'none';
            closeIt();
        }
        else {
            uploadPage.style.display = 'none';
            resultPage.style.display = 'block';
        }
    }, 5000)
}

async function displayPrediction() {
    let form = document.getElementById('image-upload-form');
    let formData = new FormData(form);

    try {
        let response = await fetch('/', {
            method: 'POST',
            body: formData
        });

        let data = await response.json()
        let prediction = data.prediction;

        document.querySelector('.predictions-card-image img').src = prediction.photo;
        document.querySelector('.description').innerHTML = `Classificamos o animal que deixou a pegada como <strong><i>${prediction.scientific_name}</i></strong>, ou como é popularmente conhecido, o <strong>${prediction.common_name}</strong>`;
        document.getElementById('view-details').setAttribute('onclick', `window.open('${prediction.details}', '_blank');`);    
    } catch(error) {
        console.error('Erro ao enviar requisição:', error);
    };
}

image.addEventListener('change', handleImageChange);

preview.addEventListener('dragover', (e) => {
    e.preventDefault();
});

preview.addEventListener('drop', (e) => {
    e.preventDefault();
    image.files = e.dataTransfer.files;
    handleImageChange()
});

document.getElementById('send-image').addEventListener('click', function() {
    displayPrediction();
});