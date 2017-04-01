var nodesList = {{ nodeSet|safe }}

  var dataList = []

  for (var i = 0; i < nodesList.length; i++) {
    var split = nodesList[i].split(";")
    dataList.push({id: split[0], label: split[1]})
  }

  var nodes = new vis.DataSet(dataList)

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 6},
    {from: 1, to: 2},
    {from: 1, to: 5},
  ]);

  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };

  var options = {
    interaction: {
      selectable: true,
      dragNodes: false
    },

    physics: {
      enabled: false
    },

    /*
    # configuration GUI
    configure: {
      filter: function (option, path) {
        if (path.indexOf('hierarchical') !== -1) { 
          return true;
        }
          return false;
      },
      showButton: false
    },
    */

    manipulation: {
      enabled: false,
      initiallyActive: false
    },

    layout: {
      hierarchical: {
        enabled:true,
        nodeSpacing:150,
        sortMethod:"directed",
        direction: "UD"
      }
    }
  };

  var network = new vis.Network(container, data, options);

  network.on("click", function (params) {
    params.event = "[original event]";
    console.log('<h2>Click event:</h2>' + JSON.stringify(params, null, 4));

    //debugger;

    if (params.nodes.length != 0) {
      var addButton = document.createElement("div");
      addButton.text = "DON"
    }

  });