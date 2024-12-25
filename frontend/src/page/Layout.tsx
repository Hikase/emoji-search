import { AppShell, Group, Title } from '@mantine/core';

import { ColorThemeControl } from '@emoji-search/component';

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <AppShell header={{ height: 60 }} padding="xl">
      <AppShell.Header>
        <Group w="100%" h="100%" px="xl" justify="space-between">
          <Title order={3}>Emoji Search 🤔</Title>
          <ColorThemeControl />
        </Group>
      </AppShell.Header>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
};
