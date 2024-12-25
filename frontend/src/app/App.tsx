import '@fontsource-variable/montserrat';
import '@mantine/core/styles.css';

import { MantineProvider } from '@mantine/core';

import { HomePage } from '@emoji-search/page/HomePage';

import { theme } from './theme';

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <HomePage />
    </MantineProvider>
  );
}
