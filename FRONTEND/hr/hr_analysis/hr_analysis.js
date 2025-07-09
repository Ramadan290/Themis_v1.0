let currentChart = null; // Store the active chart instance

document.addEventListener("DOMContentLoaded", () => {
  fetchHRData();
});

document.getElementById("ai-hr-button").addEventListener("click", () => {
  window.location.href = "/frontend/hr/ai_hr.html"; // Adjust path if needed
});

function fetchHRData() {
  fetch("/status/hr/analytics", {
    method: "GET",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data || typeof data !== "object") {
        console.error("Invalid data format from API:", data);
        alert("Failed to load HR analytics data.");
        return;
      }
      window.hrData = data;
      console.log("HR Data Loaded:", window.hrData);
    })
    .catch((error) => {
      console.error("Error fetching HR analytics:", error);
      Swal.fire({
        background: "linear-gradient(to bottom, #41295a, #2f0743)",
        icon: "error",
        title: "Oops...",
        color: "white",
        text: "Error loading HR analytics.",
        confirmButtonText: "OK",
      });
    });
}

function showChart(type) {
  if (!window.hrData) {
    alert("Data not loaded yet. Please wait...");
    return;
  }

  let labels = [],
    datasetLabel = "",
    datasetValues = [];

  switch (type) {
    case "attendance":
      if (!window.hrData.attendance_summary)
        return alert("No attendance data available.");
      labels = Object.keys(window.hrData.attendance_summary);
      datasetLabel = "Attendance Overview";
      datasetValues = Object.values(window.hrData.attendance_summary);
      break;
    case "payroll":
      if (!window.hrData.payroll_distribution)
        return alert("No payroll data available.");
      labels = Object.keys(window.hrData.payroll_distribution);
      datasetLabel = "Payroll Distribution";
      datasetValues = Object.values(window.hrData.payroll_distribution);
      break;
    case "departments":
      if (!window.hrData.employee_distribution)
        return alert("No department data available.");
      labels = Object.keys(window.hrData.employee_distribution);
      datasetLabel = "Employees per Department";
      datasetValues = Object.values(window.hrData.employee_distribution);
      break;
    case "completion_rate":
      if (!window.hrData.task_completion_distribution)
        return alert("No completion rate data available.");
      labels = Object.keys(window.hrData.task_completion_distribution);
      datasetLabel = "Task Completion Rate";
      datasetValues = Object.values(window.hrData.task_completion_distribution);
      break;
    case "workload":
      if (!window.hrData.workload_distribution)
        return alert("No workload data available.");
      labels = Object.keys(window.hrData.workload_distribution);
      datasetLabel = "Workload Distribution";
      datasetValues = Object.values(window.hrData.workload_distribution);
      break;
    case "workload_balancing":
      if (!window.hrData.workload_balancing)
        return alert("No workload balancing data available.");
      labels = Object.keys(window.hrData.workload_balancing);
      datasetLabel = "Workload Balancing";
      datasetValues = Object.values(window.hrData.workload_balancing);
      break;
    case "raise_requests":
      if (!window.hrData.raise_requests_summary)
        return alert("No raise request data available.");
      labels = Object.keys(window.hrData.raise_requests_summary);
      datasetLabel = "Raise Requests Summary";
      datasetValues = Object.values(window.hrData.raise_requests_summary);
      break;
    case "interaction_summary":
      if (!window.hrData.interaction_summary)
        return alert("No interaction data available.");
      labels = Object.keys(window.hrData.interaction_summary);
      datasetLabel = "Interaction Summary";
      datasetValues = Object.values(window.hrData.interaction_summary);
      break;
    default:
      alert("Invalid chart type");
      return;
  }

  renderChart(labels, datasetLabel, datasetValues, "bar"); // Default to bar chart
  document.getElementById("chart-container").style.display = "block";
  document.getElementById("chart-type-buttons").style.display = "block";
}

function renderChart(labels, datasetLabel, datasetValues, chartType) {
  const ctx = document.getElementById("analyticsChart").getContext("2d");

  if (currentChart) {
    currentChart.destroy();
  }

  // Auto-expand colors if needed
  const colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "cyan",
    "magenta",
    "lime",
    "teal",
    "pink",
    "brown",
  ];

  // Repeat colors if dataset is longer
  const backgroundColors = [];
  for (let i = 0; i < datasetValues.length; i++) {
    backgroundColors.push(colors[i % colors.length]);
  }

  currentChart = new Chart(ctx, {
    type: chartType,
    data: {
      labels: labels,
      datasets: [
        {
          label: datasetLabel,
          data: datasetValues,
          backgroundColor: backgroundColors,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

function updateChartType(type) {
  if (currentChart) {
    currentChart.config.type = type;
    currentChart.update();
  }
}

function closeChart() {
  document.getElementById("chart-container").style.display = "none";
  document.getElementById("chart-type-buttons").style.display = "none";

  if (currentChart) {
    currentChart.destroy();
    currentChart = null;
  }
}
