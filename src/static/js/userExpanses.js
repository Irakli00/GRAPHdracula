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

const flashes = document?.querySelector(".flashes");
if (flashes) {
  document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
      flashes.querySelector("p").style.opacity = 0;
    }, 3000);
  });
}

const asignBackgroundColors = function (data) {
  const backgroundColorsConverter = {
    Transport: "rgb(255, 255, 0)",
    Groceries: "rgb(0, 255, 0)",
    Entertainment: "rgb(187, 86, 255)",
    Healt: "rgb(86, 255, 123)",
    Bills: "rgb(255, 120, 86)",
    Travel: "rgb(255, 86, 86)",
    Shopping: "rgb(86, 125, 255)",
    Food: "rgb(255, 139, 86)",
    Health: "rgb(255, 0, 0)",
  };

  return data.map((el) => {
    if (typeof el === "string") {
      return backgroundColorsConverter[el];
    } else {
      return backgroundColorsConverter[el.category];
    }
  });
};

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

      // const backgroundColors = groupedByDate.map(
      //   (el) => backgroundColorsConverter[el.category]
      // );

      const backgroundColorsConverter = {
        Transport: "rgb(255, 255, 0)",
        Groceries: "rgb(0, 255, 0)",
        Entertainment: "rgb(187, 86, 255)",
        Healt: "rgb(86, 255, 123)",
        Bills: "rgb(255, 120, 86)",
        Travel: "rgb(255, 86, 86)",
        Shopping: "rgb(86, 125, 255)",
        Food: "rgb(255, 139, 86)",
        Health: "rgb(255, 0, 0)",
      };

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

      document.getElementById("tottal-js").textContent = `${total}$`;

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
                above: "rgba(0, 0, 255, 0.08)", // Area will be red above the origin
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
