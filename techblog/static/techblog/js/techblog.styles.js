/**
 * Created by itsmurfs on 31/08/14.
 *
 * The animations behaviors are stored here!
 */


function BlogItemSetActiveBehavior() {

    $('.blog-nav-item').each(function(){

        if (this.href === document.URL)
        {
            //Then add active class to the item clicked
            $(this).addClass('active');
        }
        else if (document.URL.search("/entry-detail/")>-1) {

            $('.blog-nav-item:contains(Blog)').addClass('active');
        }

    });

    //default behavior if no active nav bar is selected:
    if ($('.blog-nav-item.active').length==0){
        $('.blog-nav-item:contains(Blog)').addClass('active');
    }



}

function CodeLineNumberBehavior() {

    $('.linenodiv a').click(function(){

        //href is formatted like this: "#-n" where n is the line number
        line_number = this.hash.substring(2);

        id_span ="#line-"+line_number;

        //We have to find the code block of this line
        //We go on the parent table and descend to the code td column. Inside it we can find all the span elements
        //which represent a single line of code
        lighted_span = $(this).parents('table').find('.code span.light');
        if(lighted_span) {
            lighted_span.removeClass('light');
        }
        $(this).parents('table').find(id_span).addClass('light');

        return false;

    });



}

function CodeExpandBehavior(){

    $('.highlighttable tbody').hover(
        //enter
        function(){
            $(this).parents('div.highlighted').addClass('overflow_code');
        },
        //leave
        function(){
            $(this).parents('div.highlighted').removeClass('overflow_code');
        });

}

function DivContentBehavior(){

    //Fix for id_content height
    $('#id_content').height($('.row').height())
}

$(document).ready(function(){

    BlogItemSetActiveBehavior();

    CodeLineNumberBehavior();

    //DivContentBehavior();

    //CodeExpandBehavior();


});
