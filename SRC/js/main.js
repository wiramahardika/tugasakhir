// / Apply script after whole document is ready
$( document ).ready(function() {
  var requestNodes = send_ajax_request('GET', 'session/nodes.json');
  var requestEdges = send_ajax_request('GET', 'session/edges.json');

  $.when(requestNodes, requestEdges).done(function(nodes, edges){
    renderGraph(JSON.parse(nodes[0]), JSON.parse(edges[0]));
  });
});
