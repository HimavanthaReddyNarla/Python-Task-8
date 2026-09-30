const nav = document.querySelector("#task-nav");
const form = document.querySelector("#task-form");
const title = document.querySelector("#task-title");
const group = document.querySelector("#current-group");
const taskGroup = document.querySelector("#task-group");
const taskNumber = document.querySelector("#task-number");
const note = document.querySelector("#task-note");
const output = document.querySelector("#output");
const outputState = document.querySelector("#output-state");
const runButton = document.querySelector("#run-button");

let tasks = [];
let selectedTask;

const notes = {
  1: "Explore positions in a string.",
  2: "Use slices to select, skip, and reverse characters.",
  3: "Compare the original with its uppercase and lowercase forms.",
  4: "Replace every matching word in a sentence.",
  5: "Split text into a list, then print each word on its own line.",
  6: "Join a list of words with three different separators.",
  7: "Trim extra spaces and format both names consistently.",
  8: "Calculate a line-item total and format a rupee bill.",
  9: "Check a word without regard to letter case.",
  10: "Count words after splitting on whitespace.",
  11: "Inspect character, space, vowel, and consonant counts.",
  12: "Count each vowel separately, including vowels with mixed case.",
  13: "Remove every space from a sentence.",
  14: "Reverse each word while keeping the words in order.",
  15: "See several useful string facts in one report.",
};

function renderNavigation() {
  nav.replaceChildren();
  let previousGroup = "";

  for (const task of tasks) {
    if (task.group !== previousGroup) {
      const heading = document.createElement("div");
      heading.className = "task-group-label";
      heading.textContent = task.group;
      nav.append(heading);
      previousGroup = task.group;
    }

    const button = document.createElement("button");
    button.type = "button";
    button.className = "task-link";
    button.dataset.taskId = task.id;
    button.innerHTML = `<span class="task-link-number">${String(task.id).padStart(2, "0")}</span><span class="task-link-title"></span>`;
    button.querySelector(".task-link-title").textContent = task.title;
    button.addEventListener("click", () => selectTask(task.id));
    nav.append(button);
  }
}

function renderFields(task) {
  form.replaceChildren();
  const row = task.id === 8 ? document.createElement("div") : null;
  if (row) row.className = "form-row";

  for (const field of task.fields) {
    const wrapper = document.createElement("div");
    wrapper.className = "field";
    const label = document.createElement("label");
    label.htmlFor = `field-${field.name}`;
    label.textContent = field.label;
    const input = document.createElement(field.multiline ? "textarea" : "input");
    input.id = label.htmlFor;
    input.name = field.name;
    input.placeholder = field.placeholder || "";
    input.required = true;
    if (field.type) input.type = field.type;
    if (field.step) input.step = field.step;
    wrapper.append(label, input);
    (row || form).append(wrapper);
  }

  if (row) form.append(row);
}

function selectTask(taskId) {
  selectedTask = tasks.find((task) => task.id === taskId);
  if (!selectedTask) return;

  for (const button of nav.querySelectorAll(".task-link")) {
    if (Number(button.dataset.taskId) === taskId) {
      button.setAttribute("aria-current", "page");
    } else {
      button.removeAttribute("aria-current");
    }
  }

  title.textContent = selectedTask.title;
  group.textContent = selectedTask.group.toUpperCase();
  taskGroup.textContent = selectedTask.group.toUpperCase();
  taskNumber.textContent = String(taskId).padStart(2, "0");
  note.textContent = notes[taskId];
  renderFields(selectedTask);
  output.textContent = selectedTask.fields.length ? "Your result will appear here." : "Ready to run this exercise.";
  output.classList.remove("has-result");
  outputState.textContent = "READY";

  if (selectedTask.fields.length === 0) runTask();
}

async function runTask() {
  if (!selectedTask) return;
  if (!form.reportValidity()) return;

  const values = Object.fromEntries(new FormData(form).entries());
  runButton.disabled = true;
  outputState.textContent = "RUNNING";

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: selectedTask.id, values }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "The exercise could not run.");
    output.textContent = result.result;
    output.classList.add("has-result");
    outputState.textContent = "COMPLETE";
  } catch (error) {
    output.textContent = error.message;
    output.classList.remove("has-result");
    outputState.textContent = "ERROR";
  } finally {
    runButton.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  runTask();
});

async function start() {
  try {
    const response = await fetch("/api/tasks");
    if (!response.ok) throw new Error("Could not load exercises.");
    tasks = await response.json();
    renderNavigation();
    selectTask(1);
  } catch (error) {
    output.textContent = error.message;
    outputState.textContent = "ERROR";
  }
}

start();