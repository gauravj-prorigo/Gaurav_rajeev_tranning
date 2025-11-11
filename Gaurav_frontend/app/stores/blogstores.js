import { api } from "#imports";
import { defineStore } from "#imports";

export const UseBlogstore = defineStore('blog', {

    state: () => ({
        blog: [],
        loading: false,
        error: null
    }),


    actions: {
        async fetchBlogs() {
            this.loading = true
            this.error = null
            try {
                  const newBlog = await api('api/blogs/', { method: 'GET' })
                  this.loading = false
                  this.blog = newBlog
            } catch (err) {
                this.error = err.message
            } finally {
             
            }
        },


        async AddBlogs(blog) {
            try {
                const newBlog = await api('api/blogs/', { method: 'POST', body: blog })
                this.blogs.push(newBlog)
            } catch (err) {
                this.error = err.message
            }
        },


        async DeleteBlog(id) {
            try {
                await api(`api/blogs/${id}/`, { method: 'DELETE' })
                this.blog = this.blog.filter((b) => b.id === id)
            }
            catch (err) {
                this.error = err.message
            }
        },

        async UpdateBlog(id,blog) {
            try {
                const updatedBlog = await api(`api/blogs/${id}/`, { method: 'PUT', body: blog })
                const index = this.blogs.findIndex(b => b.id === id)
                if (index !== -1) this.blogs[index] = updatedBlog
            } catch (err) {
                this.error = err.message
            }
        }
    }


})