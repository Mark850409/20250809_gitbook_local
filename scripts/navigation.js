document.addEventListener("DOMContentLoaded", function() {
    // 获取页面导航元素
    var navigationElement = document.querySelector(".book-header .navigation");
    
    // 创建上一页按钮
    var previousButton = document.createElement("a");
    previousButton.innerHTML = "上一页";
    previousButton.href = "javascript:history.back()";
    navigationElement.appendChild(previousButton);

    // 创建下一页按钮
    var nextButton = document.createElement("a");
    nextButton.innerHTML = "下一页";
    nextButton.href = "javascript:history.forward()";
    navigationElement.appendChild(nextButton);
});
