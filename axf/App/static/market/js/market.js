$(document).ready(function () {
    // 获取 全部类型 和 排序的按钮节点
    var allTypes = document.getElementById('allTypes');
    var sort = document.getElementById('sort');

    // 把全部类型和排序展示的div节点获取到
    var typeDiv = document.getElementById('typeDiv');
    var sortDiv = document.getElementById('sortDiv');

    // 将 类别和排序的样式隐藏 不显示
    typeDiv.style.display = 'none';
    sortDiv.style.display = 'none';

    // 给类型和排序按钮添加点击事件
    allTypes.addEventListener('click', function () {
        typeDiv.style.display = 'block';
        sortDiv.style.display = 'none';
    });

    sort.addEventListener('click', function () {
        typeDiv.style.display = 'none';
        sortDiv.style.display = 'block';
    });

    // 给 俩个显示的div添加点击事件
    typeDiv.addEventListener('click', function () {
        typeDiv.style.display = 'none';
    });
    sortDiv.addEventListener('click', function () {
        sortDiv.style.display = 'none';
    })

});