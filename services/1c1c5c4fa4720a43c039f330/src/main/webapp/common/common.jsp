<%--
  Common include file with shared functions and variables
--%>
<%
    String basePath = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + request.getContextPath() + "/";
    pageContext.setAttribute("basePath", basePath);
%>
<script>
    var basePath = '<%=basePath%>';
</script>
<style>
    .bg-body { background-color: #f5f5f5; }
    .container { width: 1200px; margin: 0 auto; padding: 20px; }
    .box { background: #fff; padding: 20px; border-radius: 5px; }
    .fix { display: flex; margin: 15px 0; align-items: center; }
    .label { width: 120px; text-align: right; padding-right: 10px; }
    .cell { flex: 1; }
    .form-control { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; width: 100%; box-sizing: border-box; }
    .w300 { width: 300px; }
    .btn { padding: 8px 20px; border: 1px solid #ddd; background: #fff; cursor: pointer; margin-right: 10px; }
    .btn-blue { background: #007bff; color: #fff; border-color: #007bff; }
    .breadcrumb { padding: 10px 0; }
    .breadcrumb ul { list-style: none; padding: 0; margin: 0; display: flex; }
    .breadcrumb li { margin-right: 5px; }
    .split { margin: 0 5px; color: #999; }
    .active { color: #007bff; }
    .mt5 { margin-top: 5px; }
    .ml10 { margin-left: 10px; }
    .offset-x { padding-left: 120px; }
    .form-required { color: red; }
    .vn { vertical-align: middle; }
</style>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>