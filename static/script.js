/*
 * Dashboard JavaScript
 * by Emil Tullstedt
 * 2012-12-14
 */

$(function() {
	$(".eventtitle").click(function() {
		$(this).next('.detailedinfo').toggle(300);
	})
});