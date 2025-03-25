export default {
    template: `
    <b-card @click="navigate(course.id)"
              style="cursor: pointer; margin-right:15px;margin-bottom:40px;height:200px;border:1px solid #015668;
              background: url('http://localhost:5000/static/images/course_background.jpg') center/cover no-repeat;">
              <p class="card-text" style="margin-left:7px;margin-top:5px;font-size:28px; color:white;">{{course.name}}</p>
              <p v-if="course.id==1" style="margin-left:7px;margin-top:2px;font-size:14px; color:white;">NEW COURSE</p>
              <p v-else style="margin-left:7px;margin-top:2px;font-size:14px; color:white;">Coming Soon</p>
    </b-card>
    `,
    props: ['course'],
    data() {
      return {
        token: JSON.parse(localStorage.getItem('user')).token,
        role: JSON.parse(localStorage.getItem('user')).role
      }
    },
    methods: {
      navigate(courseId) {
        if (courseId === 1) {
          this.$router.push({ path: '/coursecontents', query: { id: courseId } });
        }
      }
    },
  }