async function findJobs() {
  const skills = document.getElementById("skills").value;

  if (!skills) {
    alert("Please enter at least one skill.");
    return;
  }

  // Show loading message
  const resultsList = document.querySelector(".results ul");
  resultsList.innerHTML = "<li>🔍 Searching for jobs...</li>";

  try {
    const response = await fetch("/match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skills: skills })
    });

    const data = await response.json();

    resultsList.innerHTML = ""; // clear loading

    if (data.matches && data.matches.length > 0) {
      data.matches.forEach(match => {
        const li = document.createElement("li");
        li.textContent = `${match[0]} (Matched Skills: ${match[1]})`;
        resultsList.appendChild(li);
      });
    } else {
      resultsList.innerHTML = "<li>❌ No jobs found for the given skills.</li>";
    }
  } catch (error) {
    console.error("Error fetching jobs:", error);
    resultsList.innerHTML = "<li>⚠ Error connecting to server.</li>";
  }
}