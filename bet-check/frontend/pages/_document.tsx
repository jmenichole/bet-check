import Document, {
  Html,
  Head,
  Main,
  NextScript,
  type DocumentProps,
} from 'next/document'

export default function MyDocument(props: DocumentProps) {
  return (
    <Html lang="en">
      <Head>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
