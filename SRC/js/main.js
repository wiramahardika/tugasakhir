// / Apply script after whole document is ready
$( document ).ready(function() {
  var requestNodes = send_ajax_request('GET', 'graph_data/nodes_full.json');
  var requestEdges = send_ajax_request('GET', 'graph_data/edges_full.json');

  $.when(requestNodes, requestEdges).done(function(nodes, edges){
    renderGraph(JSON.parse(nodes[0]), JSON.parse(edges[0]));
  });
});
