import { ActionIcon, AppShell, Group, rem, Title } from '@mantine/core';
import { IconBrandGithub } from '@tabler/icons-react';

import { ColorThemeControl } from '@emoji-search/component';

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <AppShell header={{ height: 60 }} padding="xl">
      <AppShell.Header>
        <Group w="100%" h="100%" px="xl" justify="space-between">
          <Title order={3}>Emoji Search 🤔</Title>
          <Group>
            <ActionIcon
              component="a"
              href="https://github.com/Hikase/emoji-search"
              variant="subtle"
              size="lg"
            >
              <IconBrandGithub style={{ width: rem(22), height: rem(22) }} stroke={2} />
            </ActionIcon>
            <ColorThemeControl />
          </Group>
        </Group>
      </AppShell.Header>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
};
