const userId = document.getElementById("totalChart").dataset.userid;
const expansesForm = document.querySelector(".expanses-form");
const flashes = document?.querySelector(".flashes");
const spendingStatus = document?.querySelector(".spending_status");
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

const asignBackgroundColors = function (data) {
  const backgroundColorsConverter = {
    Transport: "rgb(0, 128, 255)",
    Groceries: "rgb(34, 139, 34)",
    Entertainment: "rgb(255, 105, 180)",
    Health: "rgb(0, 255, 0)",
    Bills: "rgb(255, 99, 71)",
    Travel: "rgb(135, 206, 235)",
    Shopping: "rgb(255, 165, 0)",
    Food: "rgb(255, 223, 186)",
    Health: "rgb(0, 255, 0)",
  };

  return data.map((el) => {
    if (typeof el === "string") {
      return backgroundColorsConverter[el];
    } else {
      return backgroundColorsConverter[el.category];
    }
  });
};

if (flashes) {
  document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
      flashes.querySelector("p").style.opacity = 0;
    }, 3000);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  fetch(`/api/user/${userId}/expenses`)
    .then((response) => response.json())
    .then((data) => {
      if (!data) {
        console.warn("No expenses found.");
        return;
      }
      //---------

      const groupedExpenses = formatExpanses(data.expanses);
      const labels = formatLabels(data.expanses);

      console.log(data.expanses);

      const soulTrack = data.expanses.map((el) => {
        return {
          date: el.date,
          amount: el.amount,
          category: el.category,
        };
      });

      const expansesAmountData = soulTrack.reduce((acc, expense) => {
        if (!acc[expense.date]) {
          acc[expense.date] = {
            date: expense.date,
            amount: 0,
            category: expense.category,
          };
        }
        acc[expense.date].amount += expense.amount;
        return acc;
      }, {});

      const groupedByDate = Object.values(expansesAmountData);
      const expanseLabels = new Set(data.expanses.map((el) => el.date));

      const catgrs = Object.entries(groupedExpenses).map(([key, _]) => key);
      //-----

      const ctx = document.getElementById("totalChart");
      const totalChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: formatLabels(data.expanses),
          datasets: [
            {
              data: labels.map((category) => groupedExpenses[category]),
              backgroundColor: asignBackgroundColors([
                ...catgrs.map((el) => el),
              ]),

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

      console.log(data.budgets[0]);

      const month = new Date().getMonth();
      console.log(month);

      document.getElementById("tottal-js").textContent = `${total}$`;
      spendingStatus.textContent =
        data.budgets[0][`0${month + 1}`] > total
          ? `You Have ${
              data.budgets[0][`0${month + 1}`] - total
            }$ In Your Disposal`
          : `You Are ${
              total - data.budgets[0][`0${month + 1}`]
            }$ Over Your Budget`;

      //-----------------
      const ctx2 = document.getElementById("expansesChart");

      const expansesChart = new Chart(ctx2, {
        type: "line",
        data: {
          labels: [...expanseLabels],
          datasets: [
            {
              data: groupedByDate.map((el) => el.amount),
              backgroundColor: asignBackgroundColors(groupedByDate),
              borderColor: "rgb(0, 0, 0)",
              borderWidth: 0.5,
              tension: 0.2,

              fill: {
                target: "origin",
                above: "rgba(0, 0, 255, 0.08)",
              },
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
