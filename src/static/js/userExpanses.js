const userId = document.getElementById("totalChart").dataset.userid;
const expansesForm = document.querySelector(".expanses-form");
const allCharts = [];

const formatExpanses = function (expanses) {
  const groupedExpenses = expanses.reduce((acc, expense) => {
    if (!acc[expense.category]) {
      acc[expense.category] = 0;
    }
    acc[expense.category] += expense.amount;
    return acc;
  }, {});

  return groupedExpenses;
};

const formatLabels = function (data) {
  return [...new Set(data.map((expense) => expense.category))];
};

const createChart = function (ctx0, expanses) {
  const ctx = document.getElementById("totalChart"); //ctx
  const totalChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: formatLabels(expenseData),
      datasets: [
        {
          data: labels.map((category) => groupedExpenses[category]),
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 205, 86)",
            "rgb(86, 255, 123)",
            "rgb(255, 86, 255)",
            "rgb(255, 86, 86)",
            "rgb(86, 125, 255)",
          ],
          borderColor: "rgb(0, 0, 0)",
          borderWidth: 0.5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
      },
    },
  });

  allCharts.push(totalChart);
};

const convertExpanseCategory = function (num) {
  const obj = {
    1: "Food",
    2: "Transport",
    3: "Groceries",
    4: "Shoping",
    5: "Entertainment",
    6: "Travel",
    7: "Health",
    8: "Bills",
  };

  return obj[num];
};

document.addEventListener("DOMContentLoaded", function () {
  fetch(`/api/user/${userId}/expenses`)
    .then((response) => response.json())
    .then((expenseData) => {
      if (!expenseData.length) {
        console.warn("No expenses found.");
        return;
      }

      const groupedExpenses = formatExpanses(expenseData);
      const labels = formatLabels(expenseData);

      const ctx = document.getElementById("totalChart");
      const totalChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: formatLabels(expenseData),
          datasets: [
            {
              data: labels.map((category) => groupedExpenses[category]),
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(86, 255, 123)",
                "rgb(255, 86, 255)",
                "rgb(255, 86, 86)",
                "rgb(86, 125, 255)",
              ],
              borderColor: "rgb(0, 0, 0)",
              borderWidth: 0.5,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              position: "top",
            },
          },
        },
      });

      allCharts.push(totalChart);

      const total = Object.values(groupedExpenses).reduce(
        (acc, value) => acc + value,
        0
      );

      document.getElementById("tottal-js").textContent = `${total}$`;

      //-----------------
      const ctx2 = document.getElementById("expansesChart");

      const soulTrack = expenseData.map((el) => {
        return { date: el.date, amount: el.amount };
      });

      const expansesAmountData = soulTrack.reduce((acc, expense) => {
        if (!acc[expense.date]) {
          acc[expense.date] = { date: expense.date, amount: 0 };
        }
        acc[expense.date].amount += expense.amount;
        return acc;
      }, {});

      const groupedByDate = Object.values(expansesAmountData);
      // console.log(groupedByDate, expansesAmountData);
      const expanseLabels = new Set(expenseData.map((el) => el.date));

      const expansesChart = new Chart(ctx2, {
        type: "line",
        data: {
          labels: [...expanseLabels],
          datasets: [
            {
              data: groupedByDate.map((el) => el.amount),
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(86, 255, 123)",
                "rgb(255, 86, 255)",
                "rgb(255, 86, 86)",
                "rgb(86, 125, 255)",
              ],
              borderColor: "rgb(0, 0, 0)",
              borderWidth: 0.5,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });

      allCharts.push(expansesChart);
    })
    .catch((error) => console.error("Error fetching data:", error));
});

//-------------------
const statBtns = document.getElementById("sections-nav").querySelectorAll("li");
const statAreas = document
  .querySelector(".stat-area")
  .querySelectorAll(".stat-area > section");

statBtns.forEach((el, i) => {
  el.addEventListener("click", () => {
    statBtns.forEach((btn) => {
      btn.classList.remove("active");
    });
    el.classList.add("active");

    statAreas.forEach((el) => el.classList.add("hidden"));
    statAreas[el.dataset.index].classList.remove("hidden");
  });
});
//-------------------
