function updateResultBadge(resultText) {
    const badge = document.getElementById("result-badge");
    const normalized = resultText.toLowerCase();
    badge.textContent = resultText;
    badge.className = "result-badge ";
    if (normalized.includes("accepted")) {
        badge.classList.add("accepted");
    } else if (normalized.includes("wrong")) {
        badge.classList.add("wrong");
    } else if (normalized.includes("runtime") || normalized.includes("timeout")) {
        badge.classList.add("error");
    } else {
        badge.classList.add("neutral");
    }
}

function sendCode(url, editor) {
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.editorConfig.csrfToken,
        },
        body: JSON.stringify({ code: editor.getValue() }),
    }).then((response) => response.json());
}

document.addEventListener("DOMContentLoaded", () => {
    if (!window.editorConfig) {
        return;
    }

    require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs" } });
    require(["vs/editor/editor.main"], () => {
        const editor = monaco.editor.create(document.getElementById("editor"), {
            value: window.editorConfig.starterCode,
            language: "python",
            theme: "vs-dark",
            minimap: { enabled: false },
            automaticLayout: true,
            fontSize: 15,
            padding: { top: 18 },
            roundedSelection: true,
            scrollBeyondLastLine: false,
        });

        const consoleOutput = document.getElementById("console-output");

        document.getElementById("run-code-btn").addEventListener("click", async () => {
            updateResultBadge("Running...");
            const data = await sendCode(window.editorConfig.runUrl, editor);
            updateResultBadge(data.result);
            consoleOutput.textContent = data.error || data.output || "No output returned.";
        });

        document.getElementById("submit-code-btn").addEventListener("click", async () => {
            updateResultBadge("Submitting...");
            const data = await sendCode(window.editorConfig.submitUrl, editor);
            updateResultBadge(data.result);
            consoleOutput.textContent = data.error || data.output || `Passed ${data.passed}/${data.total} test cases.`;
        });
    });
});
