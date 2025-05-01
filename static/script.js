// script.js - Handles frontend interaction for ADHD Agent (v4.3 - Aside Encouragement)

document.addEventListener('DOMContentLoaded', () => {

    // Get references to elements
    const taskInput = document.getElementById('task-input');
    const submitButton = document.getElementById('submit-button');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');
    const loginPromptMessage = document.getElementById('login-prompt-message');
    const resultArea = document.getElementById('result-area'); // Area inside card for steps
    const stepsOutput = document.getElementById('steps-output');
    const stepsSection = document.getElementById('steps-section');
    // Encouragement elements moved outside the card
    const encouragementAside = document.getElementById('encouragement-aside');
    const encouragementOutput = document.getElementById('encouragement-output'); // The <p> tag inside the aside

    const errorMessageSpan = errorMessage ? errorMessage.querySelector('span') : null;
    const userWelcomeSpan = document.getElementById('user-welcome');

    // --- Event Listener for Task Decomposer Button ---
    if (submitButton) {
        submitButton.addEventListener('click', () => {
            const isLoggedIn = !!userWelcomeSpan;
            if (!isLoggedIn) {
                hideLoading(); hideError(); hideResults();
                displayLoginPrompt();
                return;
            }
            const taskDescription = taskInput ? taskInput.value.trim() : '';
            if (!taskDescription) { displayError("Please describe the objective or challenge."); return; }

            hideError(); hideLoginPrompt(); hideResults(); showLoading();
            submitButton.disabled = true;

            fetch('/decompose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', },
                body: JSON.stringify({ task_description: taskDescription })
            })
            .then(response => {
                const responseStatus = response.status;
                if (!response.ok) {
                    return response.json().then(errData => {
                        const error = new Error(errData.error || `Server error: ${response.status} ${response.statusText}`);
                        error.status = responseStatus; throw error;
                    }).catch(() => {
                        const error = new Error(`Server error: ${response.status} ${response.statusText}`);
                        error.status = responseStatus; throw error;
                    });
                }
                return response.json();
             })
            .then(data => {
                hideLoading(); submitButton.disabled = false;
                // Pass both steps and encouragement to displayResults
                if (data.steps || data.encouragement) {
                    displayResults(data.steps, data.encouragement);
                } else if (data.error) {
                     displayError(data.error);
                } else {
                    displayError("Received an unexpected response format.");
                    console.error("Unexpected data:", data);
                }
             })
            .catch(error => {
                hideLoading(); submitButton.disabled = false;
                let friendlyMessage = `An error occurred: ${error.message}`;
                if (error.status === 500) { friendlyMessage = `Server issue. Check OpenAI config/deployment.`; }
                else if (error.status === 401) { friendlyMessage = "Session expired. Please log in."; displayLoginPrompt(friendlyMessage); return; }
                displayError(friendlyMessage); console.error('Fetch error:', error);
             });
        });
    }

    // --- Event Listener for "Done" Buttons on Tasks Page ---
    document.querySelectorAll('.done-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const taskItem = event.target.closest('.task-item');
            const taskTitle = button.dataset.taskTitle || 'this task';
            if (taskItem && !taskItem.classList.contains('task-done')) {
                taskItem.classList.add('task-done');
                const actionsDiv = taskItem.querySelector('.task-actions');
                if(actionsDiv) actionsDiv.style.display = 'none';
                const encouragements = [
                    `Great job finishing "${taskTitle}"! 🎉`,
                    `Awesome work completing "${taskTitle}"! Keep the momentum going! 💪`,
                    `"${taskTitle}" done! That's fantastic progress! ✨`,
                    `You did it! "${taskTitle}" is complete. Well done! 👍`,
                    `Excellent! You knocked out "${taskTitle}". Amazing focus! 🚀`
                ];
                const randomEncouragement = encouragements[Math.floor(Math.random() * encouragements.length)];
                alert(randomEncouragement);
            }
        });
    });

    // --- Helper Functions ---
    function showLoading() { if (loadingMessage) loadingMessage.style.display = 'block'; }
    function hideLoading() { if (loadingMessage) loadingMessage.style.display = 'none'; }
    function displayError(message) {
        hideLoginPrompt(); hideResults();
        if (errorMessage && errorMessageSpan) { errorMessageSpan.textContent = " " + message; errorMessage.style.display = 'block'; }
        else { console.error("Could not display error:", message); }
    }
    function hideError() { if (errorMessage) errorMessage.style.display = 'none'; }
    function displayLoginPrompt(message = "Please sign in first to use this feature.") {
        hideError(); hideResults();
         if (loginPromptMessage) {
            const spanElement = loginPromptMessage.querySelector('span');
            if (spanElement) { spanElement.textContent = message; }
            loginPromptMessage.style.display = 'block';
        }
    }
     function hideLoginPrompt() { if (loginPromptMessage) { loginPromptMessage.style.display = 'none'; } }

    function displayResults(steps, encouragement) {
        hideLoginPrompt(); hideError();
        let stepsContent = steps || "No specific steps were generated.";
        let encouragementContent = encouragement || "";

        // Display steps inside the card
        if (stepsOutput) stepsOutput.textContent = stepsContent;
        if (stepsSection) stepsSection.style.display = 'block'; // Show steps section
        if (resultArea) resultArea.style.display = 'block'; // Show main result area in card

        // Display encouragement in the aside element
        if (encouragementOutput) encouragementOutput.textContent = encouragementContent;
        if (encouragementAside) {
            if (encouragementContent) {
                encouragementAside.style.display = 'block';
                // Use timeout to allow display:block before triggering transition
                setTimeout(() => encouragementAside.classList.add('visible'), 10);
            } else {
                encouragementAside.classList.remove('visible');
                // Optionally hide completely after fade out
                 setTimeout(() => {
                    if (!encouragementAside.classList.contains('visible')) {
                         encouragementAside.style.display = 'none';
                    }
                 }, 500); // Match CSS transition duration
            }
        }
    }

    function hideResults() {
        if (resultArea) resultArea.style.display = 'none';
        if (stepsOutput) stepsOutput.textContent = '';
        if (encouragementOutput) encouragementOutput.textContent = '';
        if (stepsSection) stepsSection.style.display = 'none';
        // Hide encouragement aside
        if (encouragementAside) {
             encouragementAside.classList.remove('visible');
             setTimeout(() => {
                 if (!encouragementAside.classList.contains('visible')) {
                      encouragementAside.style.display = 'none';
                 }
             }, 500);
        }
    }

    // --- Fade-in logic for result area (inside card) ---
    if (resultArea) {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                    if (resultArea.style.display === 'block') { requestAnimationFrame(() => { resultArea.style.opacity = 1; }); }
                    else { resultArea.style.opacity = 0; }
                }
            });
        });
        observer.observe(resultArea, { attributes: true });
     }

    // --- JS for Task Breakdown Button on Tasks Page ---
    document.querySelectorAll('.breakdown-button').forEach(button => {
        button.addEventListener('click', () => {
            const taskId = button.dataset.taskId;
            const taskTitle = button.dataset.taskTitle;
            if (taskTitle) {
                sessionStorage.setItem('taskToDecompose', taskTitle);
                window.location.href = '/';
            } else { alert('Could not get task title to break down.'); }
        });
     });

    // --- Check if we need to populate task input ---
    const taskToDecompose = sessionStorage.getItem('taskToDecompose');
    if (taskToDecompose && taskInput) {
        taskInput.value = taskToDecompose;
        sessionStorage.removeItem('taskToDecompose');
    }

}); // End of DOMContentLoaded
