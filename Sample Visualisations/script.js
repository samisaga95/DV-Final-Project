var loadTimeSeries = function($, d3, moment, selectedDept) {
  "use strict";
  console.log("Entering");
  console.log(selectedDept);
  d3.select("#controllers")
    .select("rect")
    .remove();

  d3.select("#controllers")
    .selectAll("ellipse")
    .remove();

  d3.select("#controllers")
    .selectAll("text")
    .remove();

  d3.select("#controllers")
    .selectAll("line")
    .remove();

  d3.select("#controllers")
    .selectAll("svg")
    .remove();

  var dataset = data();
  // *** THE DATA *** //
  function data() {
    var arr = [];
    d3.json("./timeline_" + selectedDept + "_5.json", function(data) {
      for (var dt in data) {
        arr.push({
          date: dt,
          values: data[dt],
          float: Math.random() * 1000
        });
      }
    });
    return arr;
  }

  var interval = setInterval(function() {
    if (dataset != null) {
      maincall();
      clearInterval(interval);
    }
  }, 1000);

  console.log(dataset);
  function maincall() {
    // *** THE COLORS / KEY *** //
    var colors = [
      ["1", "#1f77b4"],
      ["2", "#2ca02c"],
      ["3", "#ff7f0e"],
      ["4", "#FF4500"],
      ["5", "#FFA500"]
    ];

    // *** SETTINGS *** //
    var settings = (function() {
      var margins = {
        top: 10,
        bottom: 40,
        left: 40,
        right: 100
      };
      var dim = {
        width: 1000,
        height: 400
      };

      return {
        margins: margins,
        dim: dim
      };
    })();

    var renderChart = function(dataset, colors, settings) {
      // setup data for graphing ... re-map data and then stack

      var remapped = colors.map(function(c, i) {
        return dataset.map(function(d, ii) {
          return {
            x: ii,
            y: d.values[i]
          };
        });
      });
      //stack
      var stacked = d3.layout.stack()(remapped);

      // *** SCALES *** //
      var x = d3.scale
        .ordinal()
        .domain(
          stacked[0].map(function(d) {
            return d.x;
          })
        ) //pick one of the mapped arrays' x values for the domain
        .rangeRoundBands([0, 7500]);
      var y = d3.scale
        .linear()
        .domain([
          0,
          d3.max(stacked[stacked.length - 1], function(d) {
            return d.y0 + d.y;
          })
        ]) //the last mapped arrays' has the cummulative y values (y0)
        .range([0, settings.dim.height]);
      var z = d3.scale.ordinal().range(
        colors.map(function(c) {
          return c[1];
        })
      ); //ordinal scale with the colors

      // *** SETUP THE CHART *** //
      d3.select("#Tchart svg").remove(); //clear out old version
      var svg = d3
        .select("#Tchart")
        .append("svg")
        .attr({
          class: "chart-wrapper",
          width: 7000 + settings.margins.left + settings.margins.right,
          height:
            settings.dim.height + settings.margins.top + settings.margins.bottom
        });

      var Tchart = svg
        .append("g")
        .attr(
          "transform",
          "translate(" +
            settings.margins.left +
            "," +
            settings.margins.top +
            ")"
        );

      // Add a group for each column.
      var valgroup = Tchart.selectAll("g.valgroup")
        .data(stacked)
        .enter()
        .append("g")
        .attr("class", "valgroup")
        .style("fill", function(d, i) {
          return z(i);
        })
        .style("stroke", function(d, i) {
          return d3.rgb(z(i)).darker();
        });

      // Add a rect for each date.
      var rect = valgroup
        .selectAll("rect")
        .data(function(d) {
          return d;
        })
        .enter()
        .append("rect")
        .attr("x", function(d) {
          return x(d.x);
        })
        .attr("y", function(d) {
          return settings.dim.height - y(d.y0) - y(d.y);
        })
        .attr("height", function(d) {
          return y(d.y);
        })
        .attr("width", x.rangeBand());

      // *** ADD THE TIME SERIES BOTTOM AXIS *** //
      (function(svg, min, max, settings) {
        //setup the min and max as moment objects
        if (!moment.isMoment(min)) {
          min = moment(min);
          if (!min.isValid()) {
            throw new Error("Invalid min date: " + min);
          }
        }
        if (!moment.isMoment(max)) {
          max = moment(max);
          if (!max.isValid()) {
            throw new Error("Invalid max date: " + max);
          }
        }

        // *** SETUP THE TIME SERIES AXIS *** //
        var timeScale = d3.time
          .scale()
          .domain([min.toDate(), max.toDate()])
          .range([0, 7500]);

        //create the x-axis from the time scale
        var xAxis = (function(timeScale, min, max) {
          var tickInterval,
            tickFormat,
            tickStep = 1,
            duration = moment.duration(max.diff(min));
          //tickInterval = d3.time.month;
          //          tickFormat = "%b '%y";

          if (duration.asMonths() > 5) {
            tickInterval = d3.time.month;
            tickFormat = "%b '%y";
          } else if (duration.asWeeks() > 5) {
            tickInterval = d3.time.week;
            tickFormat = "%b %d";
          } else {
            tickInterval = d3.time.day;
            tickFormat = "%b %d";
            tickStep = Math.ceil(duration.days() / 10);
          }

          console.log(
            "date interval: ",
            { min: min, max: max },
            {
              months: duration.asMonths(),
              weeks: duration.asWeeks(),
              days: duration.asDays()
            },
            { interval: tickInterval, step: tickStep, format: tickFormat }
          );

          return d3.svg
            .axis()
            .orient("bottom")
            .scale(timeScale)
            .ticks(tickInterval, tickStep)
            .tickSize(1)
            .tickPadding(5)
            .tickFormat(d3.time.format(tickFormat));
        })(timeScale, min, max);

        //draw the axis
        svg
          .append("g")
          .attr("class", "x-axis")
          .attr(
            "transform",
            "translate(" +
              settings.margins.left +
              "," +
              (settings.dim.height + settings.margins.top) +
              ")"
          )
          .call(xAxis);

        var y = d3.scale
          .linear()
          .domain([0, 150])
          .range([400, 0]);

        var yAxis = d3.svg
          .axis()
          .scale(y)
          .orient("left")
          .ticks(10);

        svg
          .append("g")
          .attr("class", "y-axis")
          .attr(
            "transform",
            "translate(" +
              settings.margins.left +
              "," +
              settings.margins.top +
              ")"
          )
          .attr("stroke-width", "2")
          .call(yAxis)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Review Count")
          .style("fill", "white");
      })(svg, dataset[0].date, dataset[dataset.length - 1].date, settings);

      d3.select(".chart-wrapper")
        .selectAll("text")
        .style("fill", "white");

      return svg;
    }; // end renderChart //

    var renderSlider = function(dataset, settings, callback) {
      console.log(dataset);

      var RangeSlider = function(
        svg,
        width,
        radius,
        color,
        translater,
        callback
      ) {
        var self = this,
          elements = {
            min: { value: 0 },
            max: { value: width }
          },
          settings = {
            min: 0,
            max: width,
            radius: radius,
            offset: Math.floor(radius / 2),
            color: color,
            opacity: {
              full: 1.0,
              medium: 0.8,
              half: 0.5,
              light: 0.3
            },
            translater: translater,
            callback: callback
          };

        //build the bar
        elements.$bar = svg.append("rect").attr({
          x: settings.offset,
          width: settings.max - settings.offset * 2,
          y: settings.offset,
          height: settings.radius,
          fill: settings.color,
          "fill-opacity": settings.opacity.half
        });

        //build the handles
        elements.$min = svg
          .append("ellipse")
          .style("cursor", "pointer")
          .attr({
            cx: settings.min,
            cy: settings.radius,
            rx: settings.radius,
            ry: settings.radius,
            fill: settings.color,
            "fill-opacity": settings.opacity.medium
          });
        elements.$minText = svg
          .append("text")
          .attr({
            x: settings.min,
            y: settings.radius * 3 + settings.offset,
            fill: "white",
            "fill-opacity": settings.opacity.medium,
            "text-anchor": "middle"
          })
          .text(settings.translater.apply(self, [settings.min]).text);

        elements.$max = svg
          .append("ellipse")
          .style("cursor", "pointer")
          .attr({
            cx: settings.max,
            cy: settings.radius,
            rx: settings.radius,
            ry: settings.radius,
            fill: settings.color,
            "fill-opacity": settings.opacity.medium
          });
        elements.$maxText = svg
          .append("text")
          .attr({
            x: settings.max,
            y: settings.radius * 3 + settings.offset,
            fill: "white",
            "fill-opacity": settings.opacity.medium,
            "text-anchor": "middle"
          })
          .text(settings.translater.apply(self, [settings.max]).text);

        //expose as public properties
        self.elements = elements;
        self.settings = settings;

        //setup additional methods
        self.init();
      };

      RangeSlider.prototype.init = function() {
        var self = this,
          api = {};

        var runCallback = function(process) {
          if (self.settings.callback) {
            self.settings.callback.apply(self, [
              process,
              self.settings.translater.apply(self, [self.elements.min.value]),
              self.settings.translater.apply(self, [self.elements.max.value])
            ]);
          }
        };

        self.move = (function(self) {
          var api = {};

          var resetBar = function(x, width) {
            //no error checking
            self.elements.$bar.attr({
              x: Math.max(x - self.settings.offset, 0),
              width: Math.max(width, 0)
            });
          };

          api.$min = function(x) {
            if (x >= self.settings.min && x <= self.elements.max.value) {
              self.elements.min.value = x;
              self.elements.$min.attr("cx", x);
              self.elements.$minText
                .attr("x", x)
                .text(self.settings.translater.apply(self, [x]).text);
              resetBar(x, self.elements.max.value - x);
              runCallback("move");
            }
            return self; //chain-able
          };
          api.$max = function(x) {
            if (x >= self.elements.min.value && x <= self.settings.max) {
              self.elements.max.value = x;
              self.elements.$max.attr("cx", x);
              self.elements.$maxText
                .attr("x", x)
                .text(self.settings.translater.apply(self, [x]).text);
              resetBar(self.elements.min.value, x - self.elements.min.value);
              runCallback("move");
            }
            return self; //chain-able
          };

          return api;
        })(self);

        self.dragstart = (function(self) {
          var api = {};

          var render = function($element, $text) {
            $element.attr("fill-opacity", self.settings.opacity.full);
            $text.attr("fill-opacity", self.settings.full);
            self.elements.$bar.attr(
              "fill-opacity",
              self.settings.opacity.light
            );
            runCallback("dragstart");
          };
          api.$min = function() {
            render(self.elements.$min, self.elements.$minText);
            return self;
          };
          api.$max = function() {
            render(self.elements.$max, self.elements.$maxText);
            return self;
          };

          return api;
        })(self);

        self.dragend = (function(self) {
          var api = {};

          var render = function($element, $text) {
            $element.attr("fill-opacity", self.settings.opacity.medium);
            $text.attr("fill-opacity", self.settings.medium);
            self.elements.$bar.attr("fill-opacity", self.settings.opacity.half);
            runCallback("dragend");
          };
          api.$min = function() {
            render(self.elements.$min, self.elements.$minText);
            return self;
          };
          api.$max = function() {
            render(self.elements.$max, self.elements.$maxText);
            return self;
          };

          return api;
        })(self);

        return self;
      };

      var svg = d3
        .select("#controllers")
        .append("svg")
        .attr({
          width:
            settings.dim.width + settings.margins.left + settings.margins.right,
          height: 50
        });

      var min = moment(dataset[0].date),
        max = moment(dataset[dataset.length - 1].date),
        handles = {
          size: 12
        };

      var timeScale = d3.time
        .scale()
        .domain([min.toDate(), max.toDate()])
        .range([0, settings.dim.width]);

      //setup the svg container
      var svg = d3
        .select("#controllers")
        .append("svg")
        .attr({
          width: 1000 + settings.margins.left + settings.margins.right,
          height: 50
        });
      var g = svg
        .append("g")
        .attr("class", "x-axis")
        .attr("class", "line-slider")
        .attr("transform", "translate(" + settings.margins.left + ",0)");

      //draw the axis
      g.append("line").attr({
        x1: 0,
        y1: handles.size,
        x2: settings.dim.width,
        y2: handles.size,
        stroke: "#ccc",
        "stroke-width": 1
      });

      var translater = (function(timeScale) {
        return function(x) {
          var m = moment(timeScale.invert(x)),
            ret = {
              x: x,
              text: null,
              value: m
            };

          if (m.isValid()) {
            ret.text = m.format("MMM. DD, YYYY");
          }
          return ret;
        };
      })(timeScale);

      var slider = new RangeSlider(
        g,
        settings.dim.width,
        handles.size,
        "red",
        translater,
        callback
      );

      console.log("slider", slider);

      //setup handle dragging
      slider.elements.$min.call(
        d3.behavior
          .drag()
          .on("dragstart", slider.dragstart.$min)
          .on("drag", function() {
            slider.move.$min(d3.event.x);
          })
          .on("dragend", slider.dragend.$min)
      );
      slider.elements.$max.call(
        d3.behavior
          .drag()
          .on("dragstart", slider.dragstart.$max)
          .on("drag", function() {
            slider.move.$max(d3.event.x);
          })
          .on("dragend", slider.dragend.$max)
      );
    };

    var updateChart = (function(dataset, colors, settings) {
      //draw for the first time
      var svg = renderChart(dataset, colors, settings);

      var filterData = function(dstart, dend) {
        //because .isBetween is exclusive, adjust these boundaries
        dstart = dstart.subtract(1, "minute");
        dend = dend.add(1, "minute");

        return dataset.filter(function(d) {
          return moment(d.date).isBetween(dstart, dend);
        });
      };

      var callback = function(process, dstart, dend) {
        if (process === "dragend") {
          var data = filterData(dstart.value, dend.value);
          svg.attr("opacity", 1);
          svg = renderChart(data, colors, settings);
        } else if (process === "dragstart") {
          svg.attr("opacity", 0.5);
        }
      };

      return callback;
    })(dataset, colors, settings);

    renderSlider(dataset, settings, updateChart);
  }
};
