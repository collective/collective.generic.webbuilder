/* jshint node: true */

module.exports = function(grunt) {
    "use strict";

    // Project configuration.
    grunt.initConfig({

        // Metadata.
        pkg : grunt.file.readJSON('package.json'),
        banner : '/**\n' + '* generic webbuilder by Makina-Corpus\n'
                + '*/\n',

        // Task configuration.
        copy : {
            font : {
                expand : true,
                cwd : 'bower_components/font-awesome/',
                src : [ 'font/**', ],
                dest : '../static/'
            }
        },
        concat : {
            options : {
                banner : '<%= banner %>',
                stripBanners : false
            },
            js : {
                src : [
                        'bower_components/jquery/jquery.js',
                        'bower_components/bootstrap/dist/js/bootstrap.js'
                      ],
                dest : '../static/script.js'
            },
            minjs : {
                src : [
                        'bower_components/jquery/jquery.min.js',
                        'bower_components/bootstrap/dist/js/bootstrap.min.js'
                      ],
                dest : '../static/script.min.js'
            },
            css : {
                src : [
                        'bower_components/bootstrap/dist/css/bootstrap.css',
                        'bower_components/font-awesome/css/font-awesome.css',
                        'theme.css' ],
                dest : '../static/style.css'
            },
            mincss : {
                src : [
                       'bower_components/bootstrap/dist/css/bootstrap.min.css',
                        'bower_components/font-awesome/css/font-awesome.min.css',
                        'theme.css' ],
                dest : '../static/style.min.css'
            }
        },

        watch : {
            style : {
                files : [ 'theme.css' ],
                tasks : [ 'dist-css' ]
            }
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // JS distribution task.
    grunt.registerTask('dist-js', [ 'concat:js', 'concat:minjs' ]);

    // CSS distribution task.
    grunt.registerTask('dist-css', [ 'concat:css', 'concat:mincss' ]);

    // Full distribution task.
    grunt.registerTask('dist', [ 'copy', 'dist-css', 'dist-js' ]);

    // Default task.
    grunt.registerTask('default', [ 'dist' ]);

};
