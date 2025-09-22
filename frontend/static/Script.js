document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("skill-form");
    const input = document.getElementById("skills");
    const resultsDiv = document.getElementById("results");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // stop page reload

        const userSkills = input.value.trim();
        if (!userSkills) {
            resultsDiv.innerHTML = "<p>Please enter your skills.</p>";
            return;
        }

        try {
            const response = await fetch("/match", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "skills=" + encodeURIComponent(userSkills)
            });

            const matches = await response.json();

            if (matches.length === 0) {
                resultsDiv.innerHTML = "<p>No matching jobs found.</p>";
                return;
            }

            let html = "<h3>Matched Jobs:</h3><ul>";
            matches.forEach(match => {
                html += <li><strong>${match[0]}</strong> (Score: ${match[1]})</li>;
            });
            html += "</ul>";

            resultsDiv.innerHTML = html;
        } catch (error) {
            console.error("Error:", error);
            resultsDiv.innerHTML = "<p>Something went wrong. Please try again.</p>";
        }
    });
});
