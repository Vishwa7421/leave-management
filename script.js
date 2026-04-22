const API = "http://127.0.0.1:8000"; // change after deploy

async function applyLeave() {
  const data = {
    email: document.getElementById("email").value,
    leave_type: document.getElementById("type").value,
    start_date: document.getElementById("start").value,
    end_date: document.getElementById("end").value,
    reason: document.getElementById("reason").value,
  };

  await fetch(`${API}/apply-leave`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  alert("Leave Applied!");
}

async function updateLeave() {
  const id = document.getElementById("leaveId").value;
  const status = document.getElementById("status").value;

  await fetch(`${API}/update-leave/${id}?status=${status}`, {
    method: "POST",
  });

  alert("Leave Updated!");
}

async function getLeaves() {
  const res = await fetch(`${API}/leaves`);
  const data = await res.json();

  const list = document.getElementById("leaveList");
  list.innerHTML = "";

  data.forEach((item) => {
    const li = document.createElement("li");
    li.innerText = `ID: ${item[0]} | ${item[1]} | ${item[6]}`;
    list.appendChild(li);
  });
}
