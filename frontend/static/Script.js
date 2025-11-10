// Script.js

async function findJobs() {
  const skillsInput = document.getElementById("skills");
  const skills = skillsInput.value.trim();
  const resultsList = document.querySelector(".results ul");

  // Step 1: Validate input
  if (!skills) {
    alert("⚠ Please enter at least one skill before searching.");
    return;
  }

  // Step 2: Show loading message
  resultsList.innerHTML = "<li>🔍 Finding best matches for your skills...</li>";

  try {
    // Step 3: Send POST request to Flask backend
    const response = await fetch("/match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skills: skills }),
    });

    // Step 4: Handle non-200 responses
    if (!response.ok) {
      const errData = await response.json();
      resultsList.innerHTML = `<li>⚠ ${errData.error || "Server error occurred."}</li>`;
      return;
    }

    // Step 5: Parse the JSON response
    const data = await response.json();
    resultsList.innerHTML = ""; // Clear old results

    // Step 6: Display the matched jobs
    if (data.matches && data.matches.length > 0) {
      data.matches.forEach((match) => {
        const li = document.createElement("li");

        // For AI-based matching, the backend returns objects like { job: "...", score: ... }
        if (typeof match === "object" && match.job) {
          li.textContent = `${match.job} — Match Score: ${match.score.toFixed(2)}%`;
        } else {
          // For older tuple-style matches (["Job Name", score])
          li.textContent = `${match[0]} (Matched Skills: ${match[1]})`;
        }

        resultsList.appendChild(li);
      });
    } else {
      resultsList.innerHTML = "<li>❌ No matching jobs found for the given skills.</li>";
    }
  } catch (error) {
    console.error("Error fetching job matches:", error);
    resultsList.innerHTML = "<li>⚠ Unable to connect to the server. Please try again later.</li>";
  }
}
