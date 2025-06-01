// document.getElementById('uploadForm').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const fileInput = document.getElementById('fileInput');
//     const formData = new FormData();
//     formData.append('file', fileInput.files[0]);

//     const resultDiv = document.getElementById('result');
//     resultDiv.textContent = 'Processing...';

//     try {
//         const response = await fetch('/predict', {
//             method: 'POST',
//             body: formData
//         });

//         const data = await response.json();
//         if (data.error) {
//             resultDiv.textContent = `Error: ${data.error}`;
//         } else {
//             resultDiv.textContent = `Prediction: ${data.class}`;
//         }
//     } catch (error) {
//         resultDiv.textContent = 'An error occurred during prediction.';
//         console.error(error);
//     }
// });


document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const resultDiv = document.getElementById('result');
    const uploadedImage = document.getElementById('uploadedImage');
    const predictionText = document.getElementById('prediction');
    const stageText = document.getElementById('stage');

    // Reset results
    uploadedImage.style.display = 'none';
    predictionText.textContent = '';
    stageText.textContent = '';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            predictionText.textContent = `Error: ${data.error}`;
        } else {
            uploadedImage.src = data.image_url;
            uploadedImage.style.display = 'block';
            predictionText.textContent = `Prediction: ${data.class}`;
            stageText.textContent = `Stage: ${data.stage_info}`;
        }
    } catch (error) {
        predictionText.textContent = 'An error occurred during prediction.';
        console.error(error);
    }
});
