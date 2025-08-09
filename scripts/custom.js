require(["gitbook", "jQuery"], function(gitbook, $) {
  gitbook.events.bind("page.change", function() {
	  // 指定不顯示 Gitalk 的頁面列表
    var pagesWithoutGitalk = [
      "tags.html"
    ];
	var currentPage = window.location.pathname.split("/").pop();


    if (pagesWithoutGitalk.includes(currentPage)) {
      // 隱藏 Gitalk 容器
      $("#gitalk-container").hide();
    }
/*     // 獲取當前頁面的標題
    var currentPageTitle = $(".book-header h1").text().trim();
    console.log("currentPageTitle: " + currentPageTitle);

    // 遍歷側邊欄中的所有標題
    $(".summary .chapter").each(function() {
      var chapterLink = $(this).find("a").first();
      var chapterTitle = chapterLink.text().trim();

        // 在標題前添加勾勾符號
        if (!chapterLink.find(".read-indicator").length) {
          chapterLink.prepend("<span class='read-indicator'>✓ </span>");
        }

    }); */
  });
});
