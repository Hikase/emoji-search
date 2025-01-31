import '@fontsource-variable/montserrat';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';

import { MantineProvider } from '@mantine/core';
import { ModalsProvider } from '@mantine/modals';
import { Notifications } from '@mantine/notifications';

import { HomePage } from '@emoji-search/page/HomePage';

import { theme } from './theme';

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <ModalsProvider>
        <Notifications />
        <HomePage />
      </ModalsProvider>
    </MantineProvider>
  );
}
