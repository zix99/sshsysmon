{{!-- Fancy HTML based dashboard

Uses bootstrap and chartjs to generate static dashboard.

Meta variables:
  - title
  - theme

Colors from: http://clrs.cc/

--}}
<!DOCTYPE html>
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
		pre.cmdbox {
			max-height: 120px;
			overflow: auto;
			word-wrap: normal;
			white-space: pre;
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
		
		<a name="top"></a>

		<div class="container">
			<p class="text-right">Report generated on: <em>{{ctime}}</em></p>
		</div>

		{{#servers}}
		<div class="container">
			<a name="{{name}}"></a>
			<div class="page-header">
				<h1>{{name}}</h1>
			</div>

			<div class="container-fluid">
				<div class="row">
					{{!-- Alarms --}}
					<div class="col-xs-4 inspector">
						<h2>Alarms</h2>
						<table class="table table-condensed table-striped">
							{{#inspectors}}{{#alarms}}
							<tr>
								<td title="{{statement}}">{{name}}</td>
								<td>
									{{#if fired}}
									<span class="glyphicon glyphicon-remove" style="color: #FF4136"></span>
									{{else}}
									<span class="glyphicon glyphicon-ok" style="color: #2ECC40"></span>
									{{/if}}
								</td>
							</tr>
							{{/alarms}}{{/inspectors}}
						</table>
					</div>


					{{#inspectors}}
						<div class="col-xs-4 inspector">
							<h2>{{name}}</h2>

							{{!-- MEMORY --}}
							{{#ifEq type 'memory'}}
								<div class="col-xs-6">
									<h3>Mem</h3>
									<canvas id="memgraph-{{alphanum ../name}}" width="150" height="150"></canvas>
									<table class="table table-condensed">
										<tr><td>Free</td><td>{{metrics.mem_free}}</td></tr>
										<tr><td>Total</td><td>{{metrics.mem_total}}</td></tr>
									</table>
								</div>
								<div class="col-xs-6">
									<h3>Swap</h3>
									<canvas id="swapgraph-{{alphanum ../name}}" width="150" height="150"></canvas>
									<table class="table table-condensed">
										<tr><td>Free</td><td>{{metrics.swap_free}}</td></tr>
										<tr><td>Total</td><td>{{metrics.swap_total}}</td></tr>
									</table>
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

									var ctx = document.getElementById("memgraph-{{alphanum ../name}}").getContext("2d");
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

									var ctx = document.getElementById("swapgraph-{{alphanum ../name}}").getContext("2d");
									new Chart(ctx).Doughnut(data);
								})();
								</script>
							{{/ifEq}}

							{{!-- Disk space --}}
							{{#ifEq type 'disk'}}
								<canvas id="disk-{{alphanum ../name}}-{{alphanum name}}" width="150" height="150"></canvas>
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

									var ctx = document.getElementById("disk-{{alphanum ../name}}-{{alphanum name}}").getContext("2d");
									new Chart(ctx).Pie(data);
								})();
								</script>
								<table class="table table-striped table-condensed">
									<tr>
										<td>Used</td>
										<td>{{metrics.used}}</td>
									</tr>
									<tr>
										<td>Free</td>
										<td>{{metrics.available}}</td>
									</tr>
									<tr>
										<td>Total</td>
										<td>{{metrics.size}}</td>
									</tr>
								</table>
							{{/ifEq}}

							{{!-- Load Average --}}
							{{#ifEq type 'loadavg'}}
								<canvas id="loadavg-{{alphanum ../name}}" width="300" height="150"></canvas>
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

									var ctx = document.getElementById("loadavg-{{alphanum ../name}}").getContext("2d");
									new Chart(ctx).Bar(data);
								})();
								</script>
							{{/ifEq}}

							{{!-- TCP --}}
							{{#ifEq type 'tcp'}}
							<table class="table table-striped">
								<thead>
									<tr>
										<th>Port</th>
										<th>Status</th>
									</tr>
								</thead>
								<tbody>
									{{#each metrics}}
									<tr>
										<td>{{@key}}</td>
										<td>
											{{#if .}}
											<span class="glyphicon glyphicon-ok" style="color: #2ECC40"></span>
											{{else}}
											<span class="glyphicon glyphicon-remove" style="color: #FF4136"></span>
											{{/if}}
										</td>
									</tr>
									{{/each}}
								</tbody>
							</table>
							{{/ifEq}}

							{{!-- HTTP --}}
							{{#ifEq type 'http'}}
							<a href="{{metrics.url}}" target="_blank"><samp>{{metrics.url}}</samp></a>
							<table class="table table-striped">
								<tr>
									<td>Success</td>
									<td>
										{{#if metrics.success}}
										<span class="glyphicon glyphicon-ok" style="color: #2ECC40"></span> True
										{{else}}
										<span class="glyphicon glyphicon-remove" style="color: #FF4136"></span> False
										{{/if}}
									</td>
								</tr>
								<tr>
									<td>Status</td>
									<td><code>{{metrics.status}}</code></td>
								</tr>
							</table>

							{{#if metrics.json}}
							<pre class="cmdbox">{{metrics.json}}</pre>
							{{/if}}

							{{/ifEq}}

							{{!-- Exec --}}
							{{#ifEq type 'exec'}}
							<p>Exec: <code>{{config.command}}</code></p>
							<p>Return: <code>{{metrics.status}}</code></p>
							Stdout:
							<pre class="cmdbox">{{metrics.stdout}}</pre>
							Stderr:
							<pre class="cmdbox">{{metrics.stderr}}</pre>
							{{/ifEq}}

							{{!-- Process --}}
							{{#ifEq type 'process'}}
							{{#if metrics}}

							<table class="table table-striped">
								{{#each metrics}}
								<tr>
									<td>{{@key}}</td>
									<td>{{.}}</td>
								</tr>
								{{/each}}
							</table>

							{{else}}
							<div class="alert alert-danger">No metrics for process</div>
							{{/if}}

							{{/ifEq}}

						</div>
					{{/inspectors}}
				</div>
			</div>
		</div>
		<hr />
		{{/servers}}

		<div class="container">
			<p class="text-right"><small>Report generated by <a href="http://sshsysmon.zdyn.net/" target="_blank">SshSysMon</a> on <em>{{ctime}}</em></small></p>
		</div>

	</body>
</html>