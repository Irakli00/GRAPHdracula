const userId = document.getElementById("totalChart").dataset.userid;

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

      console.log(expenseData);

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
    })
    .catch((error) => console.error("Error fetching data:", error));
});

document
  .querySelector(".budget-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const budgetDate = document.getElementById("budgetDate").value;
    const budgetAmount = document.getElementById("budgetAmount").value;

    try {
      await fetch("/api/user/budget", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          budget_date: budgetDate,
          budget_amount: budgetAmount,
        }),
      })
        .then((res) => res.json())
        .then((d) => {
          console.log(d);
          document.querySelector(".message").textContent = d.message;
          document.querySelector(
            ".budget-for"
          ).innerHTML = `  Budget for 0${d.budget.month}, ${d.budget.year} :
          <b> ${d.budget.amount}$</b>`;
        });
    } catch (error) {
      console.error("Fetch Error:", error);
    }
  });

document
  .querySelector(".expanses-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = {
      category: document.getElementById("category").value,
      expanse_amount: document.getElementById("expanseAmount").value,
      description: document.getElementById("expanseDesc").value,
      expanse_date: document.getElementById("expanseDate").value,
    };

    try {
      await fetch("/api/user/expanses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          formData,
        }),
      }).then(() => {
        console.log(convertExpanseCategory(formData.category));
        const xExpenses = [];

        xExpenses.push({
          category: convertExpanseCategory(formData.category),
          amount: formData.expanse_amount,
        });

        const labels = [
          ...new Set(xExpenses.map((expense) => expense.category)),
        ];

        console.log(xExpenses, labels);

        if (!allCharts[0]) {
          new Chart(document.getElementById("totalChart"), {
            type: "doughnut",
            data: {
              labels: labels,
              datasets: [
                {
                  data: xExpenses,
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
                  position: "left",
                },
              },
            },
          });
        } else {
          allCharts[0].data.datasets[0].data.push(+formData.expanse_amount); // pass chart as argument latter
          allCharts[0].update();
        }
      });
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  });
