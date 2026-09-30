// ==================================================
// HELPER
// ==================================================

function getElement(id) {
    return document.getElementById(id);
}


// ==================================================
// ESCAPE HTML
// ==================================================

function escapeHtml(value) {

    return String(value)

        .replaceAll("&", "&amp;")

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


// ==================================================
// DISPLAY RESULT
// ==================================================

function showResult(
    id,
    content,
    error = false
) {

    const element =
        getElement(id);

    element.classList.remove(
        "hidden"
    );

    element.classList.toggle(
        "error",
        error
    );

    element.innerHTML =
        content;
}


// ==================================================
// DISPLAY TEXT
// ==================================================

function displayText(
    text
) {

    return `
        <pre>
${escapeHtml(text)}
        </pre>
    `;
}


// ==================================================
// API REQUEST
// ==================================================

async function apiRequest(
    endpoint,
    data
) {

    const response =
        await fetch(
            `/api/${endpoint}`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)
            }
        );


    let result;


    try {

        result =
            await response.json();

    }

    catch {

        throw new Error(
            "Invalid server response."
        );

    }


    if (!response.ok) {

        throw new Error(
            result.detail ||
            "Request failed."
        );

    }


    return result;
}


// ==================================================
// QUESTION ANSWER
// ==================================================

async function askQuestion() {

    const question =
        getElement(
            "question"
        ).value.trim();


    if (!question) {

        showResult(
            "qaResult",
            "Please enter a question.",
            true
        );

        return;

    }


    showResult(
        "qaResult",
        "🤔 Thinking..."
    );


    try {

        const result =
            await apiRequest(
                "qa",
                {
                    question:
                        question
                }
            );


        showResult(
            "qaResult",
            displayText(
                result.result
            )
        );

    }

    catch (error) {

        showResult(
            "qaResult",
            escapeHtml(
                error.message
            ),
            true
        );

    }

}


// ==================================================
// EXPLAIN
// ==================================================

async function explainTopic() {

    const topic =
        getElement(
            "topic"
        ).value.trim();


    if (!topic) {

        showResult(
            "explainResult",
            "Please enter a topic.",
            true
        );

        return;

    }


    showResult(
        "explainResult",
        "💡 Preparing explanation..."
    );


    try {

        const result =
            await apiRequest(
                "explain",
                {
                    topic:
                        topic
                }
            );


        showResult(
            "explainResult",
            displayText(
                result.result
            )
        );

    }

    catch (error) {

        showResult(
            "explainResult",
            escapeHtml(
                error.message
            ),
            true
        );

    }

}


// ==================================================
// SUMMARIZE
// ==================================================

async function summarize() {

    const text =
        getElement(
            "summaryText"
        ).value.trim();


    if (!text) {

        showResult(
            "summaryResult",
            "Please enter some notes.",
            true
        );

        return;

    }


    showResult(
        "summaryResult",
        "📝 Summarizing..."
    );


    try {

        const result =
            await apiRequest(
                "summarize",
                {
                    text:
                        text
                }
            );


        showResult(
            "summaryResult",
            displayText(
                result.result
            )
        );

    }

    catch (error) {

        showResult(
            "summaryResult",
            escapeHtml(
                error.message
            ),
            true
        );

    }

}


// ==================================================
// QUIZ
// ==================================================

async function generateQuiz() {

    const topic =
        getElement(
            "quizTopic"
        ).value.trim();


    const text =
        getElement(
            "quizText"
        ).value.trim();


    const count =
        Number(
            getElement(
                "quizCount"
            ).value
        );


    if (!topic && !text) {

        showResult(
            "quizResult",
            "Please enter a topic or study material.",
            true
        );

        return;

    }


    showResult(
        "quizResult",
        "🧠 Generating quiz..."
    );


    try {

        const result =
            await apiRequest(
                "quiz",
                {
                    topic:
                        topic,

                    text:
                        text,

                    count:
                        count
                }
            );


        showResult(
            "quizResult",
            renderQuiz(
                result.quiz
            )
        );

    }

    catch (error) {

        showResult(
            "quizResult",
            escapeHtml(
                error.message
            ),
            true
        );

    }

}


// ==================================================
// RENDER QUIZ
// ==================================================

function renderQuiz(
    quiz
) {

    return quiz
        .map(
            (item, index) => {

                const options =
                    item.options
                        .map(
                            option =>
                                `
                                <li>
                                    ${escapeHtml(
                                        option
                                    )}
                                </li>
                                `
                        )
                        .join("");


                return `

                    <article
                        class="quiz-question"
                    >

                        <h3>

                            ${index + 1}.
                            ${escapeHtml(
                                item.question
                            )}

                        </h3>


                        <ol type="A">

                            ${options}

                        </ol>


                        <details>

                            <summary>
                                Show Answer
                            </summary>


                            <p>

                                <strong>
                                    Answer:
                                </strong>

                                ${escapeHtml(
                                    item.answer
                                )}

                            </p>


                            <p>

                                ${escapeHtml(
                                    item.explanation
                                )}

                            </p>

                        </details>

                    </article>

                `;

            }
        )
        .join("");

}


// ==================================================
// LEARNING PATH
// ==================================================

async function createLearningPath() {

    const topic =
        getElement(
            "learnTopic"
        ).value.trim();


    const level =
        getElement(
            "learnLevel"
        ).value;


    if (!topic) {

        showResult(
            "learnResult",
            "Please enter a topic.",
            true
        );

        return;

    }


    showResult(
        "learnResult",
        "🗺️ Creating your learning path..."
    );


    try {

        const result =
            await apiRequest(
                "learning-path",
                {
                    topic:
                        topic,

                    level:
                        level
                }
            );


        showResult(
            "learnResult",
            displayText(
                result.result
            )
        );

    }

    catch (error) {

        showResult(
            "learnResult",
            escapeHtml(
                error.message
            ),
            true
        );

    }

}


// ==================================================
// BUTTON EVENTS
// ==================================================

document
    .querySelectorAll(
        "button[data-action]"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const action =
                        button.dataset.action;


                    if (
                        action === "qa"
                    ) {

                        askQuestion();

                    }


                    else if (
                        action === "explain"
                    ) {

                        explainTopic();

                    }


                    else if (
                        action === "summarize"
                    ) {

                        summarize();

                    }


                    else if (
                        action === "quiz"
                    ) {

                        generateQuiz();

                    }


                    else if (
                        action === "learning-path"
                    ) {

                        createLearningPath();

                    }

                }
            );

        }
    );


// ==================================================
// HEALTH CHECK
// ==================================================

async function checkHealth() {

    const status =
        getElement(
            "status"
        );


    try {

        const response =
            await fetch(
                "/api/health"
            );


        const data =
            await response.json();


        if (
            data.ai_configured
        ) {

            status.textContent =
                "● EduGenie is ready";

            status.classList.add(
                "ready"
            );

        }

        else {

            status.textContent =
                "● Server is running — Gemini API key is not configured";

            status.classList.add(
                "warning"
            );

        }

    }

    catch {

        status.textContent =
            "● Backend is not reachable";

        status.classList.add(
            "warning"
        );

    }

}


checkHealth();