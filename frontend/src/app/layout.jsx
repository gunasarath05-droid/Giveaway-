import './globals.css';

export const metadata = {
  title: 'Instagram Comment Picker - Giveaway Tool',
  description: 'Pick winners for your Instagram giveaways easily with our AI-powered comment picker.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
