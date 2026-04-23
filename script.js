const API = "http://127.0.0.1:8000";

// 🔹 Show message (no alert)
function showMsg(text) {
  const msg = document.getElementById("msg");
  msg.innerText = text;
  setTimeout(() => (msg.innerText = ""), 3000);
}

// 🔹 Switch UI
function showSection(id) {
  document
    .querySelectorAll(".section")
    .forEach((sec) => (sec.style.display = "none"));
  document.getElementById(id).style.display = "block";
}
async function signup() {
  const nameEl = document.getElementById("name");
  const emailEl = document.getElementById("email");
  const passEl = document.getElementById("password");

  const data = {
    name: nameEl.value,
    email: emailEl.value,
    password: passEl.value,
  };

  const res = await fetch(`${API}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();

  // 🔥 ALWAYS CLEAR FORM (success OR error)
  nameEl.value = "";
  emailEl.value = "";
  passEl.value = "";

  if (result.message) {
    localStorage.setItem("email", data.email);
    showMsg("Signup successful");
    showSection("register");
  } else {
    showMsg(result.error); // "Email already exists"
  }
}
async function login() {
  const data = {
    email: loginEmail.value,
    password: loginPassword.value,
  };

  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();

  if (result.message) {
    localStorage.setItem("email", data.email);
    showMsg("Login success");
    showSection("dashboard");
    getLeaves();
  } else {
    showMsg("User not found → Please Signup");
    showSection("signup");
  }
}

// 🔹 REGISTER EMPLOYEE
async function registerEmployee() {
  const data = {
    email: localStorage.getItem("email"),
    work_type: work.value,
    aadhar: aadhar.value,
    pan: pan.value,
    bank_account: bank.value,
    ifsc: ifsc.value,
  };

  await fetch(`${API}/register-employee`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  showMsg("Details saved");
  showSection("dashboard");
}

// 🔹 APPLY LEAVE
async function applyLeave() {
  const data = {
    email: localStorage.getItem("email"),
    leave_type: type.value,
    start_date: start.value,
    end_date: end.value,
    reason: reason.value,
  };

  await fetch(`${API}/apply-leave`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  showMsg("Leave Applied");

  type.value = "";
  start.value = "";
  end.value = "";
  reason.value = "";

  getLeaves();
  showSection("dashboard");
}

// 🔹 GET LEAVES
async function getLeaves() {
  const res = await fetch(`${API}/leaves`);
  const data = await res.json();

  let total = data.length;
  let pending = data.filter((l) => l[6] === "PENDING").length;
  let approved = data.filter((l) => l[6] === "APPROVED").length;

  document.getElementById("total").innerText = total;
  document.getElementById("pending").innerText = pending;
  document.getElementById("approved").innerText = approved;

  const table = document.getElementById("leaveTable");
  table.innerHTML = "";

  data.forEach((l) => {
    table.innerHTML += `
      <tr>
        <td>${l[0]}</td>
        <td>${l[1]}</td>
        <td>${l[6]}</td>
        <td>
          <button onclick="updateLeave(${l[0]}, 'APPROVED')">Approve</button>
          <button onclick="updateLeave(${l[0]}, 'REJECTED')">Reject</button>
        </td>
      </tr>`;
  });
}

// 🔹 UPDATE STATUS
async function updateLeave(id, status) {
  await fetch(`${API}/update-leave/${id}?status=${status}`, {
    method: "POST",
  });

  showMsg(`Leave ${status}`);
  getLeaves();
}

// 🔹 AUTO LOAD
window.onload = () => {
  const user = localStorage.getItem("email");

  if (!user) {
    showSection("login");
  } else {
    showSection("dashboard");
    getLeaves();
  }
};
