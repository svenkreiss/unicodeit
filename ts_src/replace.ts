// Copyright (c) 2010-2020 Sven Kreiss, Kyle Cranmer

import { combiningmarks, replacements, subsuperscripts } from './data';


export function replace(f: string): string {
    // Catch cases like \not\subset and \not\in and convert them to
    // use the combining character slash as in \slash{\subset}
    f = f.replace(/\\not(\\[A-z]+)/g, '\\slash{$1}');
    // escape combining marks with a space after the backslash
    for (const ic in combiningmarks) {
        const c = combiningmarks[ic];

        let i = -1;
        while (
            (i = f.indexOf(c[0], i+1)) > -1
            && f.indexOf("}", i+1) > i
        ) {
            f = f.slice(0, i+1) + ' ' + f.slice(i+1);
        }
    }

    // console.log(replacements);
    for (const ir in replacements) {
        const r = replacements[ir];
        // dirty way of a replaceAll():
        f = f.split(r[0]).join(r[1]);

        if (r[0].slice(-2) == '{}') {
            f = f.split('\\ '+r[0].slice(1)).join(r[1]);
        }
    }

    // expand groups of subscripts: _{01234}
    let isub = -1;
    while (
        (isub = f.indexOf("_{", isub+1)) > -1
        && f.indexOf("}", isub+1) > isub
    ) {
        f = f.slice(0, isub) + '_' + f[isub+2] + '_{' + f.slice(isub+3);
        f = f.replace('_{}', '');
    }

    // expand groups of superscripts: ^{01234}
    let isup = -1;
    while (
        (isup = f.indexOf("^{", isup+1)) > -1
        && f.indexOf("}", isup+1) > isup
    ) {
        f = f.slice(0, isup) + '^' + f[isup+2] + '^{' + f.slice(isup+3);
        f = f.replace('^{}', '');
    }

    // now replace subsuperscripts
    for (const ir in subsuperscripts) {
        const r = subsuperscripts[ir];
        // dirty way of a replaceAll():
        f = f.split(r[0]).join(r[1]);
    }

    // combining marks (unicode char modifies previous char)
    for (const ic in combiningmarks) {
        const c = combiningmarks[ic];

        let i = -1;
        while (
            (i = f.indexOf('\\ '+c[0].slice(1)+'{', i+1)) > -1
            && f.indexOf("}", i+1) > i
        ) {
            const newString = f[i+c[0].length+2] + c[1];
            f = f.slice(0,i)+newString+f.slice(i+1+c[0].length+3);
        }
    }

    return f;
}
