var gulp=require('gulp'),
	preprocess=require('gulp-preprocess');
gulp.task('api-dev',function(){
	return gulp.src('./static/js/*.js')
			   .pipe(preprocess({
			   		context:{
			   			apiUrl:'localhost:5000'
			   		}
			   }))
			   .pipe(gulp.dest('./static/'))
})