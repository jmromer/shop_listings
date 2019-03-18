const isDev = process.env.NODE_ENV === 'development'

const config = {
  serverBaseUrl: isDev ? 'http://127.0.0.1:5000' : ''
}

export default config
