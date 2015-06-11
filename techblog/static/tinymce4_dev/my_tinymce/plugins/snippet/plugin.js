/**
 * plugin.js
 *
 */

/*jshint unused:false */
/*global tinymce:true */

/**
 * Snippet plugin that adds a toolbar button and menu item in order to
 * show a dialog in which you can insert your code snippet along with a
 * description.
 */
tinymce.PluginManager.add('snippet', function(editor, url) {
	// Add a button that opens a window
	editor.addButton('snippet', {
		text: 'snippet',
		icon: false,
		onclick: function() {
			// Open window
			editor.windowManager.open({
				title: 'Add a snippet',
                width: 620,
                height: 380,
				body: [
					{type: 'textbox', multiline:'true', minHeight:200, name: 'code', label: 'Code'},
                    {type: 'textbox', name: 'description', label: 'Description' },
                    {type: 'listbox', name: 'language', label: 'Language', values: buildListItems() },
                    {type: 'textbox', name: 'file_name', label: 'File Name (Optional)'}

				],
				onsubmit: function(e) {
					// Insert content when the window form is submitted
                    html = '<div class="techblog_code" data-description="'+ e.data.description+'" ' +
                        'data-language="'+ e.data.language+'" data-file_name="'+ e.data.file_name +'">'+ '<pre>' +
                        escapeHTML(e.data.code)+'</pre>'+
                        '</div>'+
                        '<p></p>';
					editor.insertContent(html);
				}
			});
		}
	});

	// Adds a menu item to the tools menu
	editor.addMenuItem('example', {
		text: 'Example plugin',
		context: 'tools',
		onclick: function() {
			// Open window with a specific url
			editor.windowManager.open({
				title: 'TinyMCE site',
				url: url + '/dialog.html',
				width: 600,
				height: 400,
				buttons: [
					{
						text: 'Insert',
						onclick: function() {
							// Top most window object
							var win = editor.windowManager.getWindows()[0];

							// Insert the contents of the dialog.html textarea into the editor
							editor.insertContent(win.getContentWindow().document.getElementById('content').value);

							// Close the window
							win.close();
						}
					},

					{text: 'Close', onclick: 'close'}
				]
			});
		}
	});
});

function escapeHTML( string )
{
    var pre = document.createElement('pre');
    var text = document.createTextNode( string );
    pre.appendChild(text);
    return pre.innerHTML;
}

function buildListItems(inputList, itemCallback, startItems) {
		function appendItems(values, output) {
			output = output || [];

			tinymce.each(values, function(item) {
				var menuItem = {text: item.text || item.title};

				if (item.menu) {
					menuItem.menu = appendItems(item.menu);
				} else {
					menuItem.value = item.value;

					if (itemCallback) {
						itemCallback(menuItem);
					}
				}

				output.push(menuItem);
			});

			return output;
		}

		return appendItems(languages_supported, startItems || []);
	}


languages_supported = [
    /*{ text: 'ABAP', value: 'abap'},
    { text: 'ANTLR', value: 'antlr'},
    { text: 'ANTLR With ActionScript Target', value: 'antlr-as'},
    { text: 'ANTLR With C# Target', value: 'antlr-csharp'},
    { text: 'ANTLR With CPP Target', value: 'antlr-cpp'},
    { text: 'ANTLR With Java Target', value: 'antlr-java'},
    { text: 'ANTLR With ObjectiveC Target', value: 'antlr-objc'},
    { text: 'ANTLR With Perl Target', value: 'antlr-perl'},
    { text: 'ANTLR With Python Target', value: 'antlr-python'},
    { text: 'ANTLR With Ruby Target', value: 'antlr-ruby'},
    { text: 'ActionScript', value: 'as'},
    { text: 'ActionScript 3', value: 'as3'},
    { text: 'Ada', value: 'ada'},*/
    { text: 'ApacheConf', value: 'apacheconf'},
/*    { text: 'AppleScript', value: 'applescript'},
    { text: 'AspectJ', value: 'aspectj'},
    { text: 'Asymptote', value: 'asy'},
    { text: 'AutoIt', value: 'autoit'},*/
    { text: 'Awk', value: 'awk'},
    /*{ text: 'BBCode', value: 'bbcode'},
    { text: 'BUGS', value: 'bugs'},
    { text: 'Base Makefile', value: 'basemake'},*/
    { text: 'Bash', value: 'bash'},
    /*{ text: 'Bash Session', value: 'console'},*/
    { text: 'Batchfile', value: 'bat'},
    /*{ text: 'Befunge', value: 'befunge'},
    { text: 'BlitzMax', value: 'blitzmax'},
    { text: 'Boo', value: 'boo'},
    { text: 'Brainfuck', value: 'brainfuck'},
    { text: 'Bro', value: 'bro'},*/
    { text: 'C', value: 'c'},
    { text: 'C#', value: 'csharp'},
    { text: 'C++', value: 'cpp'},
    /*{ text: 'CBM BASIC V2', value: 'cbmbas'},
    { text: 'CFEngine3', value: 'cfengine3'},*/
    { text: 'CMake', value: 'cmake'},
    { text: 'COBOL', value: 'cobol'},
    /*{ text: 'COBOLFree', value: 'cobolfree'},*/
    { text: 'CSS', value: 'css'},
    { text: 'CSS+Django/Jinja', value: 'css+django'},
    /*{ text: 'CSS+Genshi Text', value: 'css+genshitext'},
    { text: 'CSS+Lasso', value: 'css+lasso'},
    { text: 'CSS+Mako', value: 'css+mako'},
    { text: 'CSS+Myghty', value: 'css+myghty'},*/
    { text: 'CSS+PHP', value: 'css+php'},
    { text: 'CSS+Ruby', value: 'css+erb'},
    /*{ text: 'CSS+Smarty', value: 'css+smarty'},*/
    { text: 'CUDA', value: 'cuda'},
    /*{ text: 'Ceylon', value: 'ceylon'},
    { text: 'Cheetah', value: 'cheetah'},
    { text: 'Clojure', value: 'clojure'},
    { text: 'CoffeeScript', value: 'coffee-script'},
    { text: 'Coldfusion HTML', value: 'cfm'},*/
    { text: 'Common Lisp', value: 'common-lisp'},
    /*{ text: 'Coq', value: 'coq'},
    { text: 'Croc', value: 'croc'},
    { text: 'Cython', value: 'cython'},
    { text: 'D', value: 'd'},*/
    { text: 'DTD', value: 'dtd'},
    /*{ text: 'Darcs Patch', value: 'dpatch'},
    { text: 'Dart', value: 'dart'},*/
    { text: 'Debian Control file', value: 'control'},
    { text: 'Debian Sourcelist', value: 'sourceslist'},
    { text: 'Delphi', value: 'delphi'},
    { text: 'Diff', value: 'diff'},
    { text: 'Django/Jinja', value: 'django'},
    /*{ text: 'Duel', value: 'duel'},
    { text: 'Dylan', value: 'dylan'},
    { text: 'Dylan session', value: 'dylan-console'},
    { text: 'DylanLID', value: 'dylan-lid'},
    { text: 'ECL', value: 'ecl'},
    { text: 'ERB', value: 'erb'},
    { text: 'Elixir', value: 'elixir'},
    { text: 'Elixir iex session', value: 'iex'},
    { text: 'Embedded Ragel', value: 'ragel-em'},
    { text: 'Erlang', value: 'erlang'},
    { text: 'Erlang erl session', value: 'erl'},
    { text: 'Evoque', value: 'evoque'},*/
    { text: 'FSharp', value: 'fsharp'},
    /*{ text: 'Factor', value: 'factor'},
    { text: 'Fancy', value: 'fancy'},
    { text: 'Fantom', value: 'fan'},
    { text: 'Felix', value: 'felix'},*/
    { text: 'Fortran', value: 'fortran'},
    /*{ text: 'FoxPro', value: 'Clipper'},
    { text: 'GAS', value: 'gas'},
    { text: 'GLSL', value: 'glsl'},
    { text: 'Genshi', value: 'genshi'},
    { text: 'Genshi Text', value: 'genshitext'},
    { text: 'Gettext Catalog', value: 'pot'},
    { text: 'Gherkin', value: 'Cucumber'},
    { text: 'Gnuplot', value: 'gnuplot'},*/
    { text: 'Go', value: 'go'},
    /*{ text: 'GoodData-CL', value: 'gooddata-cl'},
    { text: 'Gosu', value: 'gosu'},
    { text: 'Gosu Template', value: 'gst'},
    { text: 'Groff', value: 'groff'},*/
    { text: 'Groovy', value: 'groovy'},
    { text: 'HTML', value: 'html'},
    /*{ text: 'HTML+Cheetah', value: 'html+cheetah'},
    { text: 'HTML+Django/Jinja', value: 'html+django'},
    { text: 'HTML+Evoque', value: 'html+evoque'},
    { text: 'HTML+Genshi', value: 'html+genshi'},
    { text: 'HTML+Lasso', value: 'html+lasso'},
    { text: 'HTML+Mako', value: 'html+mako'},
    { text: 'HTML+Myghty', value: 'html+myghty'},*/
    { text: 'HTML+PHP', value: 'html+php'},
    /*{ text: 'HTML+Smarty', value: 'html+smarty'},*/
    { text: 'HTML+Velocity', value: 'html+velocity'},
    { text: 'HTTP', value: 'http'},
    /*{ text: 'Haml', value: 'haml'},
    { text: 'Haskell', value: 'haskell'},
    { text: 'Hxml', value: 'haxeml'},
    { text: 'Hybris', value: 'hybris'},
    { text: 'IDL', value: 'idl'},*/
    { text: 'INI', value: 'ini'},
    /*{ text: 'IRC logs', value: 'irc'},
    { text: 'Io', value: 'io'},
    { text: 'Ioke', value: 'ioke'},
    { text: 'JAGS', value: 'jags'},*/
    { text: 'JSON', value: 'json'},
    /*{ text: 'Jade', value: 'jade'},*/
    { text: 'Java', value: 'java'},
    { text: 'Java Server Page', value: 'jsp'},
    { text: 'JavaScript', value: 'js'},
    /*{ text: 'JavaScript+Cheetah', value: 'js+cheetah'},
    { text: 'JavaScript+Django/Jinja', value: 'js+django'},
    { text: 'JavaScript+Genshi Text', value: 'js+genshitext'},
    { text: 'JavaScript+Lasso', value: 'js+lasso'},
    { text: 'JavaScript+Mako', value: 'js+mako'},
    { text: 'JavaScript+Myghty', value: 'js+myghty'},*/
    { text: 'JavaScript+PHP', value: 'js+php'},
    { text: 'JavaScript+Ruby', value: 'js+erb'},
    /*{ text: 'JavaScript+Smarty', value: 'js+smarty'},
    { text: 'Julia', value: 'julia'},
    { text: 'Julia console', value: 'jlcon'},
    { text: 'Kconfig', value: 'kconfig'},
    { text: 'Koka', value: 'koka'},
    { text: 'Kotlin', value: 'kotlin'},
    { text: 'LLVM', value: 'llvm'},
    { text: 'Lasso', value: 'lasso'},
    { text: 'Lighttpd configuration file', value: 'lighty'},
    { text: 'Literate Haskell', value: 'lhs'},
    { text: 'LiveScript', value: 'live-script'},
    { text: 'Logos', value: 'logos'},
    { text: 'Logtalk', value: 'logtalk'},*/
    { text: 'Lua', value: 'lua'},
    /*{ text: 'MAQL', value: 'maql'},
    { text: 'MOOCode', value: 'moocode'},
    { text: 'MXML', value: 'mxml'},*/
    { text: 'Makefile', value: 'make'},
    /*{ text: 'Mako', value: 'mako'},
    { text: 'Mason', value: 'mason'},*/
    { text: 'Matlab', value: 'matlab'},
    /*{ text: 'Matlab session', value: 'matlabsession'},
    { text: 'MiniD', value: 'minid'},
    { text: 'Modelica', value: 'modelica'},
    { text: 'Modula-2', value: 'modula2'},
    { text: 'MoinMoin/Trac Wiki markup', value: 'trac-wiki'},
    { text: 'Monkey', value: 'monkey'},
    { text: 'MoonScript', value: 'moon'},
    { text: 'Mscgen', value: 'mscgen'},
    { text: 'MuPAD', value: 'mupad'},*/
    { text: 'MySQL', value: 'mysql'},
    /*{ text: 'Myghty', value: 'myghty'},
    { text: 'NASM', value: 'nasm'},
    { text: 'NSIS', value: 'nsis'},
    { text: 'Nemerle', value: 'nemerle'},
    { text: 'NewLisp', value: 'newlisp'},
    { text: 'Newspeak', value: 'newspeak'},*/
    { text: 'Nginx configuration file', value: 'nginx'},
    /*{ text: 'Nimrod', value: 'nimrod'},*/
    { text: 'NumPy', value: 'numpy'},
    /*{ text: 'OCaml', value: 'ocaml'},*/
    { text: 'Objective-C', value: 'objective-c'},
    { text: 'Objective-C++', value: 'objective-c++'},
    /*{ text: 'Objective-J', value: 'objective-j'},
    { text: 'Octave', value: 'octave'},
    { text: 'Ooc', value: 'ooc'},
    { text: 'Opa', value: 'opa'},
    { text: 'OpenEdge ABL', value: 'openedge'},*/
    { text: 'PHP', value: 'php'},
    /*{ text: 'PL/pgSQL', value: 'plpgsql'},
    { text: 'POVRay', value: 'pov'},*/
    { text: 'Perl', value: 'perl'},
    /*{ text: 'PostScript', value: 'postscript'},*/
    { text: 'PostgreSQL SQL dialect', value: 'postgresql'},
    { text: 'PostgreSQL console (psql)', value: 'psql'},
    /*{ text: 'PowerShell', value: 'powershell'},*/
    { text: 'Prolog', value: 'prolog'},
    /*{ text: 'Properties', value: 'properties'},
    { text: 'Protocol Buffer', value: 'protobuf'},*/
    { text: 'Puppet', value: 'puppet'},
    /*{ text: 'PyPy Log', value: 'pypylog'},*/
    { text: 'Python', value: 'python'},
    { text: 'Python 3', value: 'python3'},
    /*{ text: 'Python 3.0 Traceback', value: 'py3tb'},
    { text: 'Python Traceback', value: 'pytb'},
    { text: 'Python console session', value: 'pycon'},
    { text: 'QML', value: 'qml'},
    { text: 'RConsole', value: 'rconsole'},
    { text: 'REBOL', value: 'rebol'},
    { text: 'RHTML', value: 'rhtml'},
    { text: 'RPMSpec', value: 'spec'},
    { text: 'Racket', value: 'racket'},
    { text: 'Ragel', value: 'ragel'},
    { text: 'Ragel in C Host', value: 'ragel-c'},
    { text: 'Ragel in CPP Host', value: 'ragel-cpp'},
    { text: 'Ragel in D Host', value: 'ragel-d'},
    { text: 'Ragel in Java Host', value: 'ragel-java'},
    { text: 'Ragel in Objective C Host', value: 'ragel-objc'},
    { text: 'Ragel in Ruby Host', value: 'ragel-ruby'},
    { text: 'Raw token data', value: 'raw'},
    { text: 'Rd', value: 'rd'},
    { text: 'Redcode', value: 'redcode'},
    { text: 'RobotFramework', value: 'RobotFramework'},*/
    { text: 'Ruby', value: 'rb'},
    /*{ text: 'Ruby irb session', value: 'rbcon'},
    { text: 'Rust', value: 'rust'},
    { text: 'S', value: 'splus'},
    { text: 'SCSS', value: 'scss'},*/
    { text: 'SQL', value: 'sql'},
    /*{ text: 'Sass', value: 'sass'},
    { text: 'Scala', value: 'scala'},
    { text: 'Scalate Server Page', value: 'ssp'},
    { text: 'Scaml', value: 'scaml'},
    { text: 'Scheme', value: 'scheme'},
    { text: 'Scilab', value: 'scilab'},
    { text: 'Shell Session', value: 'shell-session'},
    { text: 'Smali', value: 'smali'},
    { text: 'Smalltalk', value: 'smalltalk'},
    { text: 'Smarty', value: 'smarty'},
    { text: 'Snobol', value: 'snobol'},
    { text: 'SourcePawn', value: 'sp'},*/
    { text: 'SquidConf', value: 'squidconf'},
    /*{ text: 'Stan', value: 'stan'},
    { text: 'Standard ML', value: 'sml'},
    { text: 'Tcl', value: 'tcl'},
    { text: 'Tcsh', value: 'tcsh'},*/
    { text: 'TeX', value: 'tex'},
    /*{ text: 'Tea', value: 'tea'},*/
    { text: 'Text only', value: 'text'},
    /*{ text: 'Treetop', value: 'treetop'},
    { text: 'TypeScript', value: 'ts'},
    { text: 'UrbiScript', value: 'urbiscript'},*/
    { text: 'VB.net', value: 'vb.net'},
    /*{ text: 'VGL', value: 'vgl'},
    { text: 'Vala', value: 'vala'},
    { text: 'Velocity', value: 'velocity'},
    { text: 'VimL', value: 'vim'},*/
    { text: 'XML', value: 'xml'},
    /*{ text: 'XML+Cheetah', value: 'xml+cheetah'},
    { text: 'XML+Django/Jinja', value: 'xml+django'},
    { text: 'XML+Evoque', value: 'xml+evoque'},
    { text: 'XML+Lasso', value: 'xml+lasso'},
    { text: 'XML+Mako', value: 'xml+mako'},
    { text: 'XML+Myghty', value: 'xml+myghty'},*/
    { text: 'XML+PHP', value: 'xml+php'},
    /*{ text: 'XML+Ruby', value: 'xml+erb'},
    { text: 'XML+Smarty', value: 'xml+smarty'},
    { text: 'XML+Velocity', value: 'xml+velocity'},*/
    { text: 'XQuery', value: 'xquery'},
    { text: 'XSLT', value: 'xslt'},
    /*{ text: 'Xtend', value: 'xtend'},*/
    { text: 'YAML', value: 'yaml'},
    { text: 'aspx-cs', value: 'aspx-cs'},
    { text: 'aspx-vb', value: 'aspx-vb'}
    /*{ text: 'autohotkey', value: 'ahk'},
    { text: 'c-objdump', value: 'c-objdump'},
    { text: 'ca65', value: 'ca65'},
    { text: 'cfstatement', value: 'cfs'},
    { text: 'cpp-objdump', value: 'cpp-objdump'},
    { text: 'd-objdump', value: 'd-objdump'},
    { text: 'dg', value: 'dg'},
    { text: 'eC', value: 'ec'},
    { text: 'haXe', value: 'hx'},
    { text: 'objdump', value: 'objdump'},
    { text: 'reStructuredText', value: 'rst'},
    { text: 'reg', value: 'registry'},
    { text: 'sqlite3con', value: 'sqlite3'},
    { text: 'systemverilog', value: 'systemverilog'},
    { text: 'verilog', value: 'verilog'},
    { text: 'vhdl', value: 'vhdl'}*/
];

/**
 * Created by itsmurfs on 08/08/2014.
 */
