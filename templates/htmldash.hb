{{!-- Fancy HTML based dashboard

Uses bootstrap and chartjs to generate static dashboard.

Meta variables:
  - title
  - theme

Colors from: http://clrs.cc/

--}}
<html>
	<head>
		<!-- Bootstrap and font awesome -->
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
		<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.6/{{coalesce meta.theme 'flatly'}}/bootstrap.min.css">
		<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
		<script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

		<!-- Chartjs -->
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.1.0/Chart.min.js"></script>

		<style type="text/css">
		.inspector {
			height: 350px;
		}
		</style>

		<title>{{coalesce meta.title 'System Summary'}}</title>
	</head>
	<body>
		<nav class="navbar navbar-inverse">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
			            <span class="sr-only">Toggle navigation</span>
			            <span class="icon-bar"></span>
			            <span class="icon-bar"></span>
			            <span class="icon-bar"></span>
			          </button>
					<a class="navbar-brand" href="#top">{{coalesce meta.title 'System Summary'}}</a>
				</div>
				<div id="navbar" class="collapse navbar-collapse">
					<ul class="nav navbar-nav">
						{{#servers}}
						<li><a href="#{{name}}">{{name}}</a></li>
						{{/servers}}
					</ul>
				</div>
			</div>
		</nav>
		
		<a name="top" />

		{{#servers}}
		<div class="container">
			<a name="{{name}}" />
			<div class="page-header">
				<h1>{{name}}</h1>
			</div>

			<div class="container-fluid">
				<div class="row">
					{{#inspectors}}
						<div class="col-xs-4 inspector">
							<h2>{{name}}</h2>

							{{!-- MEMORY --}}
							{{#ifEq type 'memory'}}
								<div class="col-xs-6">
									<h3>Mem</h3>
									<canvas id="memgraph-{{../_id}}" width="150" height="150"></canvas>
									<p>Free: {{metrics.mem_free}} / {{metrics.mem_total}}</p>
								</div>
								<div class="col-xs-6">
									<h3>Swap</h3>
									<canvas id="swapgraph-{{../_id}}" width="150" height="150"></canvas>
									<p>Free: {{metrics.swap_free}} / {{metrics.mem_total}}</p>
								</div>
								<script type="text/javascript">
								(function(){
									var data = [
										{
											value: ({{metrics.mem_total.mb}} - {{metrics.mem_free.mb}})|0,
											color: "#FF4136",
											label: "Used (MB)"
										},
										{
											value: {{metrics.mem_free.mb}}|0,
											color: "#DDDDDD",
											label: "Free (MB)"
										}
									];

									var ctx = document.getElementById("memgraph-{{../_id}}").getContext("2d");
									new Chart(ctx).Doughnut(data);
								})();

								(function(){
									var data = [
										{
											value: ({{metrics.swap_total.mb}} - {{metrics.swap_free.mb}})|0,
											color: "#FF851B",
											label: "Used (MB)"
										},
										{
											value: {{metrics.swap_free.mb}}|0,
											color: "#DDDDDD",
											label: "Free (MB)"
										}
									];

									var ctx = document.getElementById("swapgraph-{{../_id}}").getContext("2d");
									new Chart(ctx).Doughnut(data);
								})();
								</script>
							{{/ifEq}}

							{{!-- Disk space --}}
							{{#ifEq type 'disk'}}
								<canvas id="disk-{{../_id}}" width="150" height="150"></canvas>
								<script type="text/javascript">
								(function(){
									var data = [
										{
											value: {{metrics.used.gb}}|0,
											color: "#001f3f",
											label: "Used (GB)"
										},
										{
											value: {{metrics.available.gb}}|0,
											color: "#DDDDDD",
											label: "Free(GB)"
										}
									];

									var ctx = document.getElementById("disk-{{../_id}}").getContext("2d");
									new Chart(ctx).Pie(data);
								})();
								</script>
								<p>
									Used: {{metrics.used}}<br />
									Free: {{metrics.available}}<br />
									Total: {{metrics.size}}
								</p>
							{{/ifEq}}

							{{!-- Load Average --}}
							{{#ifEq type 'loadavg'}}
								<canvas id="loadavg-{{../_id}}" width="300" height="150"></canvas>
								<script type="text/javascript">
								(function(){
									var data = {
										labels: ["1m", "5m", "15m"],
										datasets: [
											{
												label: "Load",
												fillColor: "rgba(151,187,205,0.5)",
									            strokeColor: "rgba(151,187,205,0.8)",
									            highlightFill: "rgba(151,187,205,0.75)",
									            highlightStroke: "rgba(151,187,205,1)",
												data: [{{metrics.load_1m}}, {{metrics.load_5m}}, {{metrics.load_15m}}]
											}
										]
									};

									var ctx = document.getElementById("loadavg-{{../_id}}").getContext("2d");
									new Chart(ctx).Bar(data);
								})();
								</script>
							{{/ifEq}}

							{{!-- Exec --}}
							{{#ifEq type 'exec'}}
							<p>Return: <code>{{metrics.status}}</code></p>
							Stdout:
							<pre>
{{metrics.stdout}}
							</pre>
							Stderr:
							<pre>
{{metrics.stderr}}
							</pre>
							{{/ifEq}}


						</div>
					{{/inspectors}}
				</div>
			</div>
		</div>
		<hr />
		{{/servers}}

	</body>
</html>