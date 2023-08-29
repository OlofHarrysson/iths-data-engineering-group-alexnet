// This only loads global.css as of now.
import '../global.css';

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
