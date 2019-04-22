$(document).ready(function() {
  var overViewDataset = {};
  var margin = { top: 50, right: 50, bottom: 50, left: 50 };
  var width = $(".container").width();
  var height = window.innerHeight - margin.bottom - margin.top; // Use the window's height
  var maxRadius = 10;
  var data = [
    {
      word: "Sebastien",
      frequency: 1,
      sentiment: 2,
      comment: [
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format"
      ]
    },
    {
      word: "Grosjean",
      frequency: 2,
      sentiment: 4,
      comment: [
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format"
      ]
    },
    {
      word: "Sebastien",
      frequency: 4,
      sentiment: 5,
      comment: [
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format"
      ]
    },
    {
      word: "Grosjean",
      frequency: 3,
      sentiment: 1,
      comment: [
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format",
        "JSONLint is a validator and reformatter for JSON, a lightweight data-interchange format"
      ]
    }
  ];

  bubbleDisplay();
  function bubbleDisplay() {
    console.log(data);
    var margin = { top: 50, right: 50, bottom: 50, left: 50 };
    var width = window.innerWidth - margin.left - margin.right; // Use the window's width
    var height = window.innerHeight - margin.bottom - margin.top; // Use the window's height
    var maxRadius = 10;
    overViewDataset.children = data;
    console.log(overViewDataset);
    var radius = 300;
    var diameter = 600;

    var bubble = d3
      .pack(overViewDataset)
      .size([radius * 2, radius * 2])
      .padding(2);
    //create a new svg
    var svg = d3
      .select("#svgcontainer1")
      .append("svg")
      .attr("width", diameter)
      .attr("height", diameter)
      .attr("class", "bubble");

    //check players inside children
    var players = d3.hierarchy(overViewDataset).sum(function(d) {
      console.log(d.frequency);
      return d.frequency;
    });

    function color(sentiment) {}
    //create each player node which will be container for the circle
    var player = svg
      .selectAll(".player")
      .data(bubble(players).descendants())
      .enter()
      .filter(function(d) {
        return !d.children;
      })
      .append("g")
      .attr("class", "player")
      .attr("class", "zoom");

    player.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });

    //defining each circle in player nodes
    player
      .append("circle")
      .attr("r", function(d) {
        return d.r;
      })
      .attr("textShadow", 10)

      .style("fill", function(d) {
        if (d.data.sentiment == 1) {
          return "rgb(255,0,0)";
        } else if (d.data.sentiment == 2) {
          return "rgb(255,146,141)";
        } else if (d.data.sentiment == 3) {
          return "rgb(255,165,0)";
        } else if (d.data.sentiment == 4) {
          return "rgb(145,192,139)";
        } else {
          return "rgb(0,128,0)";
        }
      });

    //on click of each node
    player.on("click", function(d, i) {
      $(".review-container").html("");
      $.each(d.data.comment, function(key, val) {
        var text = "<li class='review-row'>" + val + "</li>";
        $(".review-container").append(text);
      });
      d3.event.stopPropagation();
    });
    player.selectAll("circle");

    function handleMouseOver() {
      console.log("mouse over");
    }
    //define the text in each circle

    player
      .append("text")
      .style("text-anchor", "middle")
      .attr("dy", "0.25em")

      .text(function(d) {
        return d.data.word.substring(0, d.r);
      })
      .attr("font-family", "BebasNeueRegular")
      .attr("font-size", function(d) {
        return d.r / 5;
      })
      .attr("fill", "black");
  }
});
