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
    }).then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }
        return data;
    });
}

function toggleNextButton(show) {
    const nextButton = document.getElementById("next-problem-btn");
    if (!nextButton) {
        return;
    }
    nextButton.classList.toggle("d-none", !show);
}

function setButtonsDisabled(disabled) {
    document.getElementById("run-code-btn").disabled = disabled;
    document.getElementById("submit-code-btn").disabled = disabled;
}

function updateAttemptCount(attempts) {
    const attemptCount = document.getElementById("attempt-count");
    if (!attemptCount || typeof attempts !== "number") {
        return;
    }
    attemptCount.textContent = `${attempts} attempts`;
}

function formatCaseBlock(testCase) {
    const lines = [`Case ${testCase.index}: ${testCase.status}`];

    if (testCase.input) {
        lines.push(`Input:\n${testCase.input}`);
    }
    if (testCase.expected) {
        lines.push(`Expected:\n${testCase.expected}`);
    }
    if (testCase.received) {
        lines.push(`Received:\n${testCase.received}`);
    }
    if (testCase.error) {
        lines.push(`Error:\n${testCase.error}`);
    }

    return lines.join("\n\n");
}

function formatSubmissionOutput(data) {
    if (Array.isArray(data.cases) && data.cases.length > 0) {
        return data.cases.map(formatCaseBlock).join("\n\n--------------------\n\n");
    }
    return data.error || data.output || `Passed ${data.passed}/${data.total} test cases.`;
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
        toggleNextButton(false);

        document.getElementById("run-code-btn").addEventListener("click", async () => {
            setButtonsDisabled(true);
            updateResultBadge("Running...");
            try {
                const data = await sendCode(window.editorConfig.runUrl, editor);
                updateResultBadge(data.result);
                consoleOutput.textContent = formatSubmissionOutput(data);
                updateAttemptCount(data.attempts);
            } catch (error) {
                updateResultBadge("Request Failed");
                consoleOutput.textContent = error.message;
            } finally {
                setButtonsDisabled(false);
            }
        });

        document.getElementById("submit-code-btn").addEventListener("click", async () => {
            setButtonsDisabled(true);
            updateResultBadge("Submitting...");
            try {
                const data = await sendCode(window.editorConfig.submitUrl, editor);
                updateResultBadge(data.result);
                consoleOutput.textContent = formatSubmissionOutput(data);
                updateAttemptCount(data.attempts);
                toggleNextButton(data.result.toLowerCase().includes("accepted"));
            } catch (error) {
                updateResultBadge("Request Failed");
                consoleOutput.textContent = error.message;
            } finally {
                setButtonsDisabled(false);
            }
        });
    });
});
