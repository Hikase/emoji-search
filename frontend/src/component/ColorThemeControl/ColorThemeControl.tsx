import cx from 'clsx';

import {
  ActionIcon,
  Tooltip,
  useComputedColorScheme,
  useMantineColorScheme,
  VisuallyHidden,
} from '@mantine/core';
import { IconMoon, IconSun } from '@tabler/icons-react';

import classes from './ColorSchemeControl.module.css';

export const ColorThemeControl = () => {
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme('light', {
    getInitialValueInEffect: true,
  });

  return (
    <Tooltip label={`${computedColorScheme === 'dark' ? 'Light' : 'Dark'} mode`}>
      <ActionIcon
        onClick={() => setColorScheme(computedColorScheme === 'light' ? 'dark' : 'light')}
        aria-label="Switch theme"
        size="md"
      >
        <VisuallyHidden>Switch theme</VisuallyHidden>
        <IconSun className={cx(classes.light, classes['icon-size-md'])} stroke={2} />
        <IconMoon className={cx(classes.dark, classes['icon-size-md'])} stroke={2} />
      </ActionIcon>
    </Tooltip>
  );
};
