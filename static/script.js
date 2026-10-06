// ============================================================
// AI RESOURCE INTELLIGENCE
// FRONTEND JAVASCRIPT
// ============================================================


// ============================================================
// ELEMENTS
// ============================================================

const fileInput =
    document.getElementById("fileInput");

const selectedFile =
    document.getElementById("selectedFile");

const analyseButton =
    document.getElementById("analyseButton");

const loadingCard =
    document.getElementById("loadingCard");

const resultsSection =
    document.getElementById("resultsSection");

const dropZone =
    document.getElementById("dropZone");


// ============================================================
// SELECT FILE
// ============================================================

fileInput.addEventListener(
    "change",
    function () {

        if (!this.files.length) {

            return;

        }


        const file =
            this.files[0];


        selectedFile.innerHTML =
            `📄 ${file.name}`;


        analyseButton.disabled =
            false;

    }
);


// ============================================================
// DRAG & DROP
// ============================================================

dropZone.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        dropZone.style.borderColor =
            "#2563eb";

    }
);


dropZone.addEventListener(
    "dragleave",
    function () {

        dropZone.style.borderColor =
            "#cbd5e1";

    }
);


dropZone.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();


        dropZone.style.borderColor =
            "#cbd5e1";


        const files =
            event.dataTransfer.files;


        if (!files.length) {

            return;

        }


        const file =
            files[0];


        fileInput.files =
            files;


        selectedFile.innerHTML =
            `📄 ${file.name}`;


        analyseButton.disabled =
            false;

    }
);


// ============================================================
// ANALYSE RESOURCE
// ============================================================

analyseButton.addEventListener(
    "click",
    async function () {

        if (!fileInput.files.length) {

            return;

        }


        const file =
            fileInput.files[0];


        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        // ----------------------------------------------------
        // UI STATE
        // ----------------------------------------------------

        analyseButton.disabled =
            true;

        loadingCard.classList.remove(
            "hidden"
        );

        resultsSection.classList.add(
            "hidden"
        );


        try {

            const response =
                await fetch(
                    "/api/upload",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const result =
                await response.json();


            if (!result.success) {

                throw new Error(
                    result.message
                    ||
                    "Analysis failed."
                );

            }


            displayResults(
                result
            );


        } catch (error) {

            alert(
                "Error: " +
                error.message
            );

        } finally {

            loadingCard.classList.add(
                "hidden"
            );

            analyseButton.disabled =
                false;

        }

    }
);


// ============================================================
// DISPLAY RESULTS
// ============================================================

function displayResults(result) {

    const analysis =
        result.analysis;


    // --------------------------------------------------------
    // Analytics
    // --------------------------------------------------------

    displayAnalytics(
        analysis.analytics
    );


    // --------------------------------------------------------
    // Summary
    // --------------------------------------------------------

    document.getElementById(
        "summaryText"
    ).textContent =
        analysis.summary;


    // --------------------------------------------------------
    // Skills
    // --------------------------------------------------------

    displaySkills(
        analysis.skills
    );


    // --------------------------------------------------------
    // Insights
    // --------------------------------------------------------

    displayInsights(
        analysis.insights
    );


    // --------------------------------------------------------
    // Career Matches
    // --------------------------------------------------------

    displayCareers(
        analysis.career_matches
    );


    // --------------------------------------------------------
    // Show results
    // --------------------------------------------------------

    resultsSection.classList.remove(
        "hidden"
    );


    resultsSection.scrollIntoView({
        behavior: "smooth"
    });

}


// ============================================================
// DISPLAY ANALYTICS
// ============================================================

function displayAnalytics(analytics) {

    const container =
        document.getElementById(
            "analyticsGrid"
        );


    const cards = [

        {
            icon: "📄",
            value: analytics.character_count,
            label: "Characters"
        },

        {
            icon: "📝",
            value: analytics.word_count,
            label: "Words"
        },

        {
            icon: "📊",
            value: analytics.sentence_count,
            label: "Sentences"
        },

        {
            icon: "🧠",
            value: analytics.skill_categories,
            label: "Skill Categories"
        },

        {
            icon: "🛠️",
            value: analytics.total_detected_skills,
            label: "Detected Skills"
        }

    ];


    container.innerHTML =
        cards.map(
            card => `

                <div class="analytics-card">

                    <div class="icon">
                        ${card.icon}
                    </div>

                    <div class="value">
                        ${card.value}
                    </div>

                    <div class="label">
                        ${card.label}
                    </div>

                </div>

            `
        ).join("");

}


// ============================================================
// DISPLAY SKILLS
// ============================================================

function displaySkills(skills) {

    const container =
        document.getElementById(
            "skillsContainer"
        );


    container.innerHTML = "";


    Object.entries(skills).forEach(
        ([category, skillList]) => {

            const categoryDiv =
                document.createElement(
                    "div"
                );


            categoryDiv.className =
                "skill-category";


            const title =
                document.createElement(
                    "h4"
                );


            title.textContent =
                category;


            categoryDiv.appendChild(
                title
            );


            skillList.forEach(
                skill => {

                    const tag =
                        document.createElement(
                            "span"
                        );


                    tag.className =
                        "skill-tag";


                    tag.textContent =
                        skill;


                    categoryDiv.appendChild(
                        tag
                    );

                }
            );


            container.appendChild(
                categoryDiv
            );

        }
    );

}


// ============================================================
// DISPLAY INSIGHTS
// ============================================================

function displayInsights(insights) {

    const container =
        document.getElementById(
            "insightsContainer"
        );


    container.innerHTML = "";


    if (!insights.length) {

        container.innerHTML =
            "<p>No major insights detected yet.</p>";

        return;

    }


    insights.forEach(
        insight => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "insight-item";


            item.textContent =
                "💡 " + insight;


            container.appendChild(
                item
            );

        }
    );

}


// ============================================================
// DISPLAY CAREER MATCHES
// ============================================================

function displayCareers(careers) {

    const container =
        document.getElementById(
            "careerContainer"
        );


    container.innerHTML = "";


    Object.entries(careers).forEach(
        ([role, information]) => {

            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "career-row";


            row.innerHTML = `

                <div class="career-header">

                    <span>
                        ${role}
                    </span>

                    <span>
                        ${information.score}%
                    </span>

                </div>


                <div class="progress">

                    <div
                        class="progress-bar"
                        style="width: ${information.score}%">
                    </div>

                </div>

            `;


            container.appendChild(
                row
            );

        }
    );

}


// ============================================================
// RAG PLACEHOLDER
// ============================================================

function askQuestion() {

    alert(
        "RAG Knowledge Assistant will be connected in the next development stage."
    );

}